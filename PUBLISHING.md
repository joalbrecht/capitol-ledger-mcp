# Publishing the adapter

This public repository contains only the local MCP adapter. The private API and
product application are maintained separately. Never add production keys,
subscriber/application data, private deployment files, or raw filings here.

## PyPI trusted publisher: one-time account setup

In the owner's PyPI account, add a **pending publisher** for a new project:

- PyPI project name: `capitol-ledger-mcp`
- GitHub owner: `joalbrecht`
- GitHub repository: `capitol-ledger-mcp`
- Workflow filename: `publish.yml`
- Environment name: `pypi`

Use https://pypi.org/manage/account/publishing/ . The account owner must confirm
this security-sensitive trust relationship themselves. No long-lived API token
is needed. The GitHub workflow exchanges short-lived OIDC identity credentials
with PyPI, scoped to this project/workflow/environment.

## Release

1. Keep `pyproject.toml`, `server.json` and its package version in sync. Verify CI.
2. Create a GitHub Release for the matching `vVERSION` tag, or manually run
   **Publish PyPI and MCP Registry** on `main` for the first release.
3. The workflow builds/tests, checks distributions, publishes to PyPI using trusted
   publishing, then uses GitHub OIDC to publish the MCP Registry metadata.
4. Verify the package/version through PyPI's JSON API and install the published
   wheel into a clean environment. Check an MCP handshake and tool list without
   using real customer credentials.
5. Verify the registry response at
   `https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.joalbrecht/capitol-ledger-mcp`.

The PyPI README includes the required registry ownership token:
`mcp-name: io.github.joalbrecht/capitol-ledger-mcp`.
Do not remove it. The registry lists installable package metadata; it does not
host the package and this server has no public remote MCP endpoint.

If PyPI succeeds but the registry step fails, retry with the separate
**Publish MCP Registry only** workflow. Do not attempt to re-upload the same
PyPI version, which is immutable.

The official publisher is pinned to v1.8.1 and its downloaded archive checksum
is checked. Publishing credentials are short-lived OIDC tokens; never print or
commit them.

## Glama

Add https://github.com/joalbrecht/capitol-ledger-mcp on
https://glama.ai/mcp/servers using **Add Server**. Sign-in and any new account or
permission approvals are completed by the owner. `glama.json` identifies
`joalbrecht` as the maintainer. The repository's MIT license, installation guide,
metadata and locally discoverable tools support indexing checks.

Do not submit a fictional remote URL or give Glama production API credentials.
The adapter can start and list its three tools without an API key; actual data
calls require approved pilot access. Submission and publication are distinct;
verify listing status before claiming the server is indexed.
