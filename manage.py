#!/usr/bin/env python
import os
import sys

from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ov_wag.settings.dev')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
