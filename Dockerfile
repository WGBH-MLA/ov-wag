# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.10-slim-buster as base

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

# Build the production image, with the application server
FROM base as production

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=80

EXPOSE 80

# Install the application server.
RUN pip install "gunicorn>=20.1.0,<20.2.0"

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
# CMD set -xe; python manage.py migrate --noinput; gunicorn ov_wag.wsgi:application --reload
COPY . .
