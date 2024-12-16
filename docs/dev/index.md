# Development

## `ov`

The `ov` script is the primary Open Vault command line script. This contains a number of pre-built commands to do basic operations.

### Usage

`ov COMMAND [args]`

```bash title="ov --help"
COMMANDS:

  b | build           build the docker images
  c | cmd             run a compose command
  cover | coverage    Run the test suite with coverage
  d | dev             start a development server
  m | manage          run a wagtail manage.py command
  s | shell           run a django shell command with the app context
  t | test            Run the test suite
  tui                 Run an interactive TUI
```

### Commands

#### `b` | `build`

: Build the docker images locally.

!!! abstract "Pass options to docker build"

    Additional docker arguments can be passed to this command.

    For example, to force a rebuild of the images:

    ```bash
    ov b --no-cache
    ```

#### `c` | `cmd`

: Run a `docker compose` command with the base config files in place.

#### `d` | `dev`

: Run Development Environment

: Run the development environment, with `docker compose`, and follow container logs.

!!! abstract "Pass options to docker compose"

    Additional compose arguments can be passed. For example, to rebuild the containers before running:

    ```bash
    ov d --build
    ```

#### `m` | `manage`

: Run a `manage.py` command in the docker context.

#### `s` | `shell`

: Enter into a python django shell interpreter, with the application context loaded.

### Show the logs

Show the docker compose logs
```bash
ov c logs
```

Show logs for just the frontend
```bash
ov c logs ov-frontend
```

## Examples

The following are some useful examples of development commands that might be run:

- [Database migrations](./migrate)
- [Fix database records](./fix_AAPBRecords)
