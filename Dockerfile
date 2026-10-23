FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY pyproject.toml README.md LICENSE capitol_ledger_mcp.py ./
RUN python -m pip install . && useradd --create-home --uid 10001 mcp
USER mcp
CMD ["capitol-ledger-mcp"]
