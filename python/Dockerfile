# The commerce-router CLI in a container.
# Kept simple on purpose; Day 38 hardens it (multi-stage, non-root user, SBOM, scan).
FROM python:3.12-slim

# Copy the uv binary from uv's official image. Same version as your laptop and CI.
COPY --from=ghcr.io/astral-sh/uv:0.11.33 /uv /uvx /bin/

WORKDIR /app

# UV_COMPILE_BYTECODE: precompile .py files so the CLI starts faster.
# UV_LINK_MODE=copy: copy files out of uv's cache instead of hard-linking (avoids a warning).
# UV_PYTHON_DOWNLOADS=never: use this image's Python 3.12, never download another.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Layer 1: dependencies only. Rebuilt only when pyproject.toml or uv.lock change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project --no-dev

# Layer 2: your code. Editing a .py file rebuilds only from here, which takes seconds.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Put the project's virtual environment first on PATH, so "ask" is the CLI uv installed.
ENV PATH="/app/.venv/bin:$PATH"

# "docker run IMAGE <args>" becomes "ask <args>".
ENTRYPOINT ["ask"]