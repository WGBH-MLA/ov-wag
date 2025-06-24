# Development

This section describes the development environment and how to use it.

## Run server
To run the development server, use the following command:

```bash
./scripts/dev
```

This will start a local development server. You can access the Wagtail admin interface at [localhost:8000/admin/](http://localhost:8000/admin/)

## Maintenance
See the [maintenance guide](./maintenance.md) for instructions on how to maintain the project, including running scripts, tests, and creating lockfiles.

For Docker users, see the [Docker maintenance guide](./docker.md) for instructions on using the `ov` helper tool for running common commands.

## Migrations
See the [migrations guide](./migrate.md) for instructions on how to manage database migrations.

## Examples
Some specific example scripts are included, such as the [`fix_AAPBRecords` notebook](./fix_AAPBRecords.ipynb) which can be used to fix AAPB records in the database. This notebook is a Jupyter notebook and can be run with Jupyter Lab or Jupyter Notebook.