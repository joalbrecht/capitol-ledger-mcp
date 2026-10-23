# Capitol Ledger MCP

Read-only **congressional stock disclosure research for AI agents**. Search official
U.S. House disclosures, inspect saved synthetic disclosure-ledger portfolios, and
explain portfolio changes with source and timing context.

[Request pilot access](https://capitol-ledger.com/agents#pilot) ·
[API documentation](https://capitol-ledger.com/agents.md) ·
[Public fictional sample](https://capitol-ledger.com/api/agents/sample) ·
[Methodology](https://capitol-ledger.com/methodology)

<!-- mcp-name: io.github.joalbrecht/capitol-ledger-mcp -->

## Access

The adapter is open source. The hosted data API requires an approved Capitol Ledger
API key. Request an invited **free 14-day pilot** at the link above. Approved pilot
accounts default to 1,000 authenticated requests per UTC day, shared across keys.
No payment details or automatic paid conversion. Submitting an application does
not grant access or subscribe you to a newsletter.

The public JSON sample is fictional and requires no key. It is useful for inspecting
the response shape; it is not a real disclosure or live data.

## Install

Python **3.12 or later** is required. Install from this public repository:

```sh
pip install 'git+https://github.com/joalbrecht/capitol-ledger-mcp.git'
```

The package name for the PyPI release is `capitol-ledger-mcp`. After that release
is available, install with `pip install capitol-ledger-mcp` or run with
`uvx --from capitol-ledger-mcp capitol-ledger-mcp`.

## Connect your MCP client

For an installed adapter, use this local stdio configuration:

```json
{
  "mcpServers": {
    "capitol-ledger": {
      "command": "capitol-ledger-mcp",
      "env": {
        "CAPITOL_LEDGER_API_URL": "https://capitol-ledger.com",
        "CAPITOL_LEDGER_API_KEY": "YOUR_APPROVED_API_KEY"
      }
    }
  }
}
```

Replace the placeholder locally and keep the key in your client's secret store.
Do not put it in a shared prompt, URL, issue, or public repository. If your client
cannot find the command, use its absolute installation path.

A client using `uvx` after the PyPI release can instead use `"command": "uvx"` and
`"args": ["--from", "capitol-ledger-mcp", "capitol-ledger-mcp"]`, with the same env.
This is a **local stdio server** that calls a hosted HTTPS API. It is not a hosted
remote MCP endpoint. No broker or trading-account credentials are needed.

## Tools

| Tool | Purpose | Parameters |
| --- | --- | --- |
| `search_disclosures` | Search House stock disclosures with filing links and amount ranges | Optional `ticker`, `side`, `available_after`, `as_of`, `limit`, `offset` |
| `get_portfolio` | Opening/closing allocations for a saved synthetic ledger report | Optional `report_id`, `as_of` |
| `get_portfolio_changes` | Purchases, sales, and allocation changes for a saved period | Optional `report_id`, `as_of` |

Example questions after connecting:

- What NVDA purchases were disclosed in the last 30 days? Include source links.
- Show the latest saved synthetic disclosure portfolio and its period.
- What changed in that report? Use the same report ID.

Search defaults to 30 days, with at most 100 rows per call. `side` accepts `purchase`,
`sale`, or `exchange`. Timestamps must include a timezone. Reuse returned `as_of`
and `available_after` when paging with `meta.next_offset`. Pin `report_id` to compare
a portfolio and its changes over the same period.

## Coverage and interpretation

- **House only.** Senate data is excluded.
- Disclosures are delayed. The transaction date, public filing availability, and
  collection time are separate; do not describe a newly filed disclosure as a trade
  that just happened.
- Disclosed amounts are ranges, not exact transaction values. Synthetic ledger
  values use midpoint estimates.
- Portfolio snapshots represent a synthetic disclosure ledger, **not** actual member
  holdings or Capitol Ledger's executable strategy portfolio. Reports may be daily,
  weekly, monthly, or ad hoc; inspect returned period metadata.
- Preserve source URLs, calculation metadata, freshness, and coverage warnings.
  Completeness is not guaranteed. Historical queries use current parsed records,
  not a complete versioned archive of parser/source revisions.
- Research data only; no personalized investment advice or order execution.
- Pilot access is for internal research workflows; contact Capitol Ledger about
  redistribution or serving downstream users. The code's MIT license does not grant
  redistribution rights to the hosted data.

## Usage and errors

All three tools use the API's account-wide quota. Usage and expiry can be checked
outside MCP using authenticated `GET /api/v1/account` (this also consumes a call).

- 401: invalid/revoked key.
- 403: inactive/expired access.
- 404: no completed saved report for that query.
- 422: invalid parameters.
- 429: daily quota exhausted; see the HTTP API's `Retry-After` header.

The tools never change subscriptions, rotate keys, submit orders, or access a local
product database. API calls require HTTPS except for local development; redirects
are not followed with credentials. Keys are environment credentials, not tool inputs.
Model inference runs in your MCP client; this adapter only retrieves research data.

## Development

```sh
pip install -e '.[dev]'
pytest
ruff check .
```

Tests use mocked HTTP and do not need live credentials or consume API quota.

## Publishing

See [PUBLISHING.md](PUBLISHING.md) for the release workflow, PyPI trusted publisher
setup, and official MCP Registry metadata. Directory submissions are not evidence
of endorsement or listing approval.

## License and contact

MIT for the adapter code. Hosted API access and data rights are separate.
Contact: [hello@capitol-ledger.com](mailto:hello@capitol-ledger.com).
