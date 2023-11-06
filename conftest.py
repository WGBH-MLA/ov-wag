from os import environ as env

env['DJANGO_SETTINGS_MODULE'] = 'ov_wag.settings.test'
env['OV_DB_HOST'] = 'localhost'
env['OV_DB_PORT'] = '5432'
env['OV_DB_NAME'] = 'ov'
env['OV_DB_USER'] = 'postgres'
env['OV_DB_PASSWORD'] = 'postgres'
