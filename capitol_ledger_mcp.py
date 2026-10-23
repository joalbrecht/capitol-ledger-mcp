"""Local MCP adapter. Credentials stay in the environment, outside tool arguments."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

import httpx


def api_get(path: str, params: dict[str, Any]) -> dict[str, Any]:
    base = os.environ.get("CAPITOL_LEDGER_API_URL", "https://capitol-ledger.com").rstrip("/")
    url = urlparse(base)
    if url.username or url.password or url.query or url.fragment or url.path not in {"", "/"}:
        raise ValueError("CAPITOL_LEDGER_API_URL must be an origin without credentials or a path")
    if url.scheme != "https" and not (
        url.scheme == "http" and url.hostname in {"localhost", "127.0.0.1", "::1"}
    ):
        raise ValueError("Use HTTPS for the agent API (HTTP is allowed only on localhost)")
    key = os.environ.get("CAPITOL_LEDGER_API_KEY", "")
    if not key:
        raise ValueError("Set CAPITOL_LEDGER_API_KEY in the MCP server environment")
    try:
        with httpx.Client(timeout=30, follow_redirects=False) as client:
            response = client.get(
                base + path,
                params={k: v for k, v in params.items() if v is not None},
                headers={"Authorization": f"Bearer {key}"},
            )
    except httpx.HTTPError:
        raise ValueError("Unable to reach Capitol Ledger. Check the API URL and retry.") from None
    if response.status_code != 200:
        # Never include response/request objects or their Authorization headers in errors.
        raise ValueError(
            f"Capitol Ledger returned HTTP {response.status_code}. Check access, quota, and query parameters."
        )
    payload: dict[str, Any] = response.json()
    return payload


def create_mcp() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        raise RuntimeError("Install the adapter and dependencies with: pip install capitol-ledger-mcp") from None

    from mcp.types import ToolAnnotations

    server = FastMCP(
        "Capitol Ledger",
        instructions=(
            "Read-only House congressional disclosure research. Always distinguish transaction dates "
            "from filing availability; cite source_url and preserve coverage warnings. Disclosed amounts "
            "are ranges. Portfolio results are synthetic ledger snapshots, not actual holdings or orders."
        ),
    )
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)

    @server.tool(annotations=annotations)
    def search_disclosures(
        ticker: str | None = None,
        side: str | None = None,
        available_after: str | None = None,
        as_of: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search House disclosures; dates use filing availability. Return source links and amount ranges.

        Default window is 30 days. Maximum limit is 100. Reuse returned as_of when paging.
        Timestamps must include a UTC offset; side is purchase, sale, or exchange.
        """
        return api_get("/api/v1/disclosures", locals())

    @server.tool(annotations=annotations)
    def get_portfolio(report_id: str | None = None, as_of: str | None = None) -> dict[str, Any]:
        """Get a saved synthetic disclosure ledger's opening/closing allocations and audit metadata.

        Defaults to latest saved completed period, of any cadence. Pin report_id for reproducibility.
        This is not actual member holdings or the executable strategy portfolio.
        """
        return api_get("/api/v1/portfolio", locals())

    @server.tool(annotations=annotations)
    def get_portfolio_changes(
        report_id: str | None = None, as_of: str | None = None
    ) -> dict[str, Any]:
        """Get purchases, sales, and weight changes for a saved report period; inspect coverage warnings.

        Pass the portfolio result's report_id to use exactly the same period.
        """
        return api_get("/api/v1/changes", locals())

    return server


def main() -> None:
    """Entry point used by the independently downloadable adapter."""
    create_mcp().run(transport="stdio")
