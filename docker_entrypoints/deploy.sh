#!/bin/bash

gunicorn ov_wag.wsgi:application --reload --access-logfile /logs/access.log --error-logfile /logs/error.log
