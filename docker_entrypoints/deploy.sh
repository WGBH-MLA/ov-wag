#!/bin/bash

# Run the production server
gunicorn ov_wag.wsgi:application \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  # --access-logfile /logs/access.log \
  --error-logfile -
  # --error-logfile /logs/error.log
