FROM ubuntu:latest

ARG YOUR_ENV
SHELL [ "/bin/bash", "-c" ]

ENV YOUR_ENV=${YOUR_ENV} \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # Required to fix a UnicodeError in tests from the rich lib
  PYTHONIOENCODING=utf-8 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry
  POETRY_VERSION="1.1.13" \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME='/usr/local' \
  PATH="${PATH}:/usr/local" \
  # other
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
  curl \
  python3-dev \
  python3-pip \
  python3-venv \
  sudo \
  && apt clean

RUN apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -U 'pip'
RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR /workspace
COPY pyproject.toml /workspace
COPY poetry.lock /workspace
COPY .flake8 /workspace

RUN poetry install --no-ansi --no-root
