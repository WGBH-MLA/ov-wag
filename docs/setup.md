# Setup

## Prerequisites
This page describes how to run the development environment. You can run the development environment locally, or in a docker container.

### Local
This is the recommended way to run the development environment, for ease of use and speed.
- `python`
- `pip`
- Running Postgres image

Use pip to install [PDM](https://pdm.fming.dev/), the package manager used for this project.

```bash
pip install pdm
```

Install the dependencies with PDM

```bash
pdm install
```

You can now run the `ov` command to interact with the development environment.

???+ question "Help! How do I ... ?"
    For a full list of available commands, run 
    ```bash
    ov -h
    ```

    For additional information, see the [dev#ov](dev.md#ov) section of the development documentation.


???+ cmd "Activate virtual environment"
    If you are not already in a virtual environment, activate the one created by PDM.

    ```bash
    $(pdm venv activate)
    ```
### Database
The development environment requires a running Postgres database. The easiest way to run this is with a docker container.

```bash
docker run --name ov-db -e POSTGRES_PASSWORD="YOUR POSTGRES PASSWORD HERE" -p 5432:5432 -d postgres:alpine
```

### Docker
The development environment can also be run in docker containers, which includes a database configuration.
- `docker compose` installed


???+ abstract "Requirements"

    - [docker](https://docs.docker.com/get-docker/)
    - [docker compose](https://docs.docker.com/compose/install/)

    Running the services outside of docker is possible, but not supported in this context.

## Setup
### 0. Clone repository
    
```bash title="Clone repository"
git clone https://github.com/WGBH-MLA/ov-wag.git
```

### 1. Create the backend secrets file

In `ov-wag`, create a file called `.env` with the following contents:

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

### 5. Start the frontend

!!! todo "Add frontend setup instructions"
    Make this link work! [ov-frontend setup](https://wgbh-mla.github.io/ov-frontend/dev/)