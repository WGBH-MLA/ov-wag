#!/bin/bash
# Migrate the database, if needed
python manage.py migrate --noinput

# NOTE: this is a background process that will keep the container running.
python manage.py runserver 0.0.0.0:80
