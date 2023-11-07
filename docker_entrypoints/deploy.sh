#!/bin/bash
cd /app/
# Build static files for the admin site
python3 manage.py collectstatic --noinput

# Run the production server
gunicorn ov_wag.wsgi:application \
  -b 0.0.0.0:8000 \
  --workers 2 \
  --forwarded-allow-ips '*' \
  --access-logfile - \
  --error-logfile -
  # --access-logfile /logs/access.log \
  # --error-logfile /logs/error.log
