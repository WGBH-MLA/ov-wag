# Maintenance

This page describes how to maintain the project. This includes [running scripts](#scripts), [creating lockfiles](#lockfiles), and [running tests](#tests).


## Scripts

There are several scripts that can be run directly from the command line. They can be run by running:

```bash
./scripts/<script_name>
```

### Common scripts
- `./scripts/dev` - Starts a local development server on port 8000
- `./scripts/docs` - Builds and serves the documentation locally
- `./scripts/docs-version` - Updates the documentation version number to match the app version
- `./scripts/makemigrations` - Creates new migrations based on the changes made to the models
- `./scripts/migrate` - Applies the migrations to the database. See the [migrations guide](./migrate.md) for more information.

### Management
All Django / Wagtail management commands can be run using the `manage.py` script:

```bash
python manage.py <command>
```

For a complete list of commands, run:

```bash
python manage.py
```


## Tests
Run the tests:

```bash
pytest
```

## Lockfiles
Update the lockfile:

```bash
uv lock
```
