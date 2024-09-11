# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11-slim as base

WORKDIR /app
COPY docker_entrypoints /docker_entrypoints

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pdm.lock README.md manage.py ./
COPY authors authors
COPY cli cli
COPY exhibits exhibits
COPY home home
COPY ov_collections ov_collections
COPY ov_wag ov_wag
COPY search search

### Test ###
# Build the test image, which includes the test applications
FROM base as test
# Install the test requirements
RUN pip install pdm
RUN pdm install -dG test

ENTRYPOINT /docker_entrypoints/test.sh

### Production ###
# Build the production image, with the application server
FROM base as production

# Create directory for logs
RUN mkdir -p /logs

# Set environment variables
# 1. Force Python stdout and stderr streams to be unbuffered
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command
ENV PYTHONUNBUFFERED=1 \
    PORT=80

EXPOSE 80

# Install the application server
RUN pip install .[production]

ENTRYPOINT /docker_entrypoints/deploy.sh
