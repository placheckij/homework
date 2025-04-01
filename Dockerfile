FROM python:3.11.7-slim-bullseye AS base

USER root
RUN apt update && apt upgrade -y \
    && apt install -y wget \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=true
RUN groupadd -g 1888 taskgroup && \
    useradd -rm -d /task -g taskgroup -u 1888 taskuser
USER taskuser
WORKDIR /task

FROM base AS poetry
RUN python -m pip install poetry==2.1.1
ENV PATH=/task/.local/bin:$PATH \
    POETRY_VIRTUALENVS_IN_PROJECT=true
COPY --chown=taskuser:taskgroup ./pyproject.toml ./poetry.lock ./README.md ./
RUN /task/.local/bin/poetry install --no-root --no-ansi --no-interaction
RUN /task/.local/bin/poetry sync

FROM base AS runtime
ENV PATH=/task/.venv/bin:$PATH
COPY --chown=taskuser:taskgroup --from=poetry /task/.venv /task/.venv
COPY --chown=taskuser:taskgroup . .

ENTRYPOINT ["/task/.venv/bin/uvicorn", "--host", "0.0.0.0", "--port", "3000", "--log-config", "app/core/logging_setup.json", "--log-level", "info", "--workers", "1", "--lifespan", "on", "app.main:app"]
