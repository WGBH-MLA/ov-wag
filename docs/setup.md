# Setup

This page describes how to run the development environment. You can run the development environment locally, or in a docker container.

## Clone repository
    
```bash title="Clone repository"
git clone https://github.com/WGBH-MLA/ov-wag.git
```

```bash title="Change directory"
cd ov-wag
```

## Local
This is the recommended way to run the development environment, for ease of use and speed.

### Prerequisites
Use pip to install [uv](https://docs.astral.sh/uv/), the package manager used for this project.

```bash
pip install uv
```

### Install
Create a new virtual environment:
```bash title="Create virtual environment"
# Create a new virtual environment
uv venv
# Activate the virtual environment
source .venv/bin/activate
```

#### Install dependencies
Install the dependencies:

```bash
uv sync
```

You can now run project commands like `python manage.py <command>` or the shortcuts in the `./scripts/` directory.

See the [maintenance section](maintenance.md) for examples of running tests, building documentation, and more.

## Database
The development environment requires a running Postgres database. The easiest way to run this is with a docker container.

```bash
docker run --name ov-db -e POSTGRES_PASSWORD="YOUR POSTGRES PASSWORD HERE" -p 5432:5432 -d postgres:alpine
```

## Docker
If local installation is not an option, a docker compose environment is provided, but we recommend using the [local installation](#local) for development if possible.


### `ov` CLI
A helper CLI is provided to make it easier to run the development environment. It is called `ov`, and can be used to run commands in the docker container.

```bash
ov <command>
```

Use `ov -h` to see the available commands and usage.


???+ abstract "Requirements"

    - [docker](https://docs.docker.com/get-docker/)
    - [docker compose](https://docs.docker.com/compose/install/)


### 1. Create the backend secrets file

In the root directory, create a file called `.env` with the following contents:

```bash title="ov-wag/.env"
OV_DB_ENGINE=django.db.backends.postgresql
OV_DB_PORT=5432
OV_DB_NAME=ov
OV_DB_USER=postgres
OV_DB_PASSWORD="YOUR POSTGRES PASSWORD HERE"

OV_BASE_URL=http://localhost:3000
OV_ADMIN_BASE_URL=http://localhost:8000
```

### 2. (Optional) Build the backend
If you have local changes, you can build the backend image locally:
```bash title="Build the backend"
ov b
```

### 3. Start the backend

```bash title="Start the backend"
ov d
```
You can now visit the admin interface at [http://localhost:8000/admin](http://localhost:8000/admin)

### 4. Create a superuser
```bash title="Create a superuser"
ov m createsuperuser
```

Follow the prompts to create an admin user.

### Next steps
See the [maintenance documentation](maintenance.md) for more information on how to run the project, including running tests, building documentation, and more.
