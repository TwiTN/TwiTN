FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


FROM node AS frontend
COPY ./www /www

WORKDIR /www
RUN npm install && npm run build

# 1. Match the builder image exactly
FROM python:3.14-slim-trixie

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

# 2. Ensure session directory exists and is writable
RUN mkdir -p /tmp/sessions && chown nonroot:nonroot /tmp/sessions

COPY --from=builder --chown=nonroot:nonroot /app /app
COPY --from=frontend --chown=nonroot:nonroot /www/dist /app/www/dist

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
USER nonroot

EXPOSE 8000

# 3. Use an explicit path to the app object to avoid ambiguity
CMD ["gunicorn", "-w", "4", "main:create_app()", "--bind", "0.0.0.0:8000"]
