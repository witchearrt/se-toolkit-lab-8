# Nanobot Gateway Dockerfile
# Multi-stage build with uv

ARG REGISTRY_PREFIX_DOCKER_HUB

# ---
# Stage 1: Build the application
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy local packages
COPY mcp-lms-local ./mcp-lms-local
COPY mcp-obs-local ./mcp-obs-local

# Copy webchat dependencies
COPY nanobot-webchat ./nanobot-webchat
COPY mcp-webchat ./mcp-webchat
COPY nanobot-channel-protocol ./nanobot-channel-protocol

# Create virtual environment
RUN uv venv

# Install local MCP servers
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./mcp-lms-local ./mcp-obs-local

# Install webchat dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install ./nanobot-webchat ./mcp-webchat

# Install nanobot from URL
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

# Copy application code
COPY entrypoint.py ./entrypoint.py
COPY config.json ./config.json
COPY workspace/ ./workspace/

# ---
# Stage 2: Runtime image
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install gosu for running as non-root
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set working directory
WORKDIR /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER nonroot

# Expose ports
EXPOSE 18790 8765

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1

# Default command
ENTRYPOINT ["python", "/app/entrypoint.py"]
