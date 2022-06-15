#!/bin/bash

python manage.py migrate --noinput
# NOTE: this is a background process that will keep the container running.
gunicorn ov_wag.wsgi:application --reload
