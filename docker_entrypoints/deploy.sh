#!/bin/bash

gunicorn ov_wag.wsgi:application --reload
