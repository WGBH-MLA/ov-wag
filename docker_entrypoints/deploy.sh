#!/bin/bash
cd /app/
# Build static files for the admin site
python3 manage.py collectstatic --noinput

# Run the production server
gunicorn ov_wag.wsgi:application \
  --access-logfile - \
  --error-logfile -
  # --access-logfile /logs/access.log \
  # --error-logfile /logs/error.log
