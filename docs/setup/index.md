# Setup

This section describes how to setup a local development environment. See the [Docker setup guide](docker.md) for instructions on how to use a Docker development environment.

It is highly recommended to run the development environment locally, for ease of use and speed.

## Clone repository
    
```bash title="Clone repository"
git clone https://github.com/WGBH-MLA/ov-wag.git
```

```bash title="Change directory"
cd ov-wag
```

## Local

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

See the [maintenance section](../dev/maintenance.md) for examples of running tests, building documentation, and more.

## Database
The development environment requires a running Postgres database. The easiest way to run this is with a docker container.

```bash
docker run --name ov-db -e POSTGRES_PASSWORD="YOUR POSTGRES PASSWORD HERE" -p 5432:5432 -d postgres:alpine
```


### Next steps
See the [development documentation](../dev/) for more information on how to run the project, including running tests, building documentation, and more.
