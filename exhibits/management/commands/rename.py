"""Rename module
Shamelessly copied from https://gist.github.com/rafaponieman/201054ddf725cda1e60be3fe845850a5
"""

import argparse

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Renames app. Usage rename_app [old_name] [new_name] [classes ...]'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('old_name', nargs=1, type=str)
        parser.add_argument('new_name', nargs=1, type=str)
        parser.add_argument('models', nargs=argparse.REMAINDER, type=str)

    def handle(self, old_name, new_name, models, *args, **options):
        with connection.cursor() as cursor:
            # Rename model
            old_name = old_name[0]
            new_name = new_name[0]
            cursor.execute(
                f"UPDATE django_content_type SET app_label='{new_name}' WHERE app_label='{old_name}'"  # noqa E501
            )
            cursor.execute(
                f"UPDATE django_migrations SET app='{new_name}' WHERE app='{old_name}'"
            )

            for model_name in models:
                cursor.execute(
                    f"ALTER TABLE {old_name}_{model_name} RENAME TO {new_name}_{model_name}"  # noqa E501
                )
