# ---- builder ----
    FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

    ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
    
    WORKDIR /app
    
    COPY pyproject.toml uv.lock ./
    RUN uv sync --frozen --no-dev
    
    COPY src/ ./src/
    
    # ---- runtime ----
    FROM python:3.13-slim
    
    RUN adduser --disabled-password --gecos "" appuser
    
    COPY --from=builder --chown=appuser /app /app
    WORKDIR /app
    
    USER appuser
    
    ENV PATH="/app/.venv/bin:$PATH"
    
    EXPOSE 8000
    
    CMD ["uvicorn", "src.main.app:app", "--host", "0.0.0.0", "--port", "8000"]
    