import asyncio

import httpx
import pytest

from capitol_ledger_mcp import api_get, create_mcp


def test_mcp_exposes_three_read_only_tools_with_no_credentials_in_arguments():
    pytest.importorskip("mcp")

    async def inspect():
        server = create_mcp()
        tools = await server.list_tools()
        assert {tool.name for tool in tools} == {
            "search_disclosures",
            "get_portfolio",
            "get_portfolio_changes",
        }
        for tool in tools:
            assert tool.annotations.readOnlyHint is True
            assert "api_key" not in tool.inputSchema["properties"]

    asyncio.run(inspect())


def test_adapter_sends_credentials_only_in_headers_and_does_not_follow_redirects(monkeypatch):
    seen = []

    def handle(request):
        seen.append(request)
        return httpx.Response(200, json={"data": [], "meta": {"coverage": "house"}})

    original = httpx.Client
    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: original(transport=transport, **kwargs))
    monkeypatch.setenv("CAPITOL_LEDGER_API_URL", "https://ledger.example")
    monkeypatch.setenv("CAPITOL_LEDGER_API_KEY", "secret-example")
    assert api_get("/api/v1/disclosures", {"ticker": "NVDA", "side": None})["data"] == []
    assert seen[0].headers["authorization"] == "Bearer secret-example"
    assert "secret-example" not in str(seen[0].url)
    assert str(seen[0].url) == "https://ledger.example/api/v1/disclosures?ticker=NVDA"


@pytest.mark.parametrize(
    "url",
    ["http://public.example", "https://user:password@example.com", "https://example.com?token=x"],
)
def test_adapter_rejects_unsafe_api_origins(monkeypatch, url):
    monkeypatch.setenv("CAPITOL_LEDGER_API_URL", url)
    with pytest.raises(ValueError):
        api_get("/api/v1/portfolio", {})
