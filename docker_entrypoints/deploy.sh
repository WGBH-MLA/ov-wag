#!/bin/bash

# Build static files for the admin site
python3 manage.py collectstatic --noinput

# Run the production server
gunicorn ov_wag.wsgi:application \
  --reload \
  --access-logfile /logs/access.log \
  --error-logfile /logs/error.log
