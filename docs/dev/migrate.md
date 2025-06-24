
# Migrate database
The following commands are used to manage database migrations in the OpenVault project. They can be run from the command line using `manage.py`.

???+ abstract "Database migrations"
    Make sure you have the correct environment set up and the database is running before executing these commands.

## Show all database migrations

```bash
python manage.py showmigrations
```

## Generate the migration files

```bash
python manage.py makemigrations
```

## Run the database migrations

```bash
python manage.py migrate
```
