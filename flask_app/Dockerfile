# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.13-slim-bookworm AS base

# ----------------
# build stage
# ----------------
FROM base AS build

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv requirements --exclude-markers > requirements.txt

# ----------------
# actual image
# ----------------
FROM base

# Add user that will be used in the container.
RUN useradd flask

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Flask.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==23.0.0"

# Install the project requirements.
COPY --from=build requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "flask" user.
RUN chown flask:flask /app

# Copy the source code of the project into the container.
COPY --chown=flask:flask . .

# Use user "flask" to run the build commands below and the server itself.
USER flask

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Flask instance can be started with a simple "docker run" command.
CMD set -xe; flask db upgrade; gunicorn 'app:create_app()'
