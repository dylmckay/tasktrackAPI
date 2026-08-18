# Get image with uv preinstalled
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Seting working directory
WORKDIR /app

# Copy & install dependencies first
COPY pyproject.toml /app/

COPY uv.lock /app/

RUN uv sync --frozen

# Then copy everything else
COPY . /app/

# Run FastAPI app (uvicorn)
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0"]