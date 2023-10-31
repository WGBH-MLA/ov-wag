#!/bin/bash

# Build static files for the admin site
python3 manage.py collectstatic --noinput

# Run the production server
gunicorn -w 2 --worker-class uvicorn.workers.UvicornWorker \
  --reload \
  --access-logfile /logs/access.log \
  --error-logfile /logs/error.log \
  ov_wag.asgi:application
