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

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Run FastAPI app (uvicorn)
ENTRYPOINT [ "/app/entrypoint.sh" ]