from os import path
from unittest import TestCase


class EnvTests(TestCase):
    def test_media_dir(self):
        """
        Test if MEDIA_ROOT directory exists

        debug: ls -la MEDIA_ROOT
        """
        from ov_wag.settings.base import MEDIA_ROOT

        self.assertTrue(path.isdir(MEDIA_ROOT))

        # Uncomment to show media directory in logs

    def test_env(self):
        """Test if the environment variables are set"""
        from os import environ as env

        self.assertTrue(env.get('DJANGO_SETTINGS_MODULE') == 'ov_wag.settings.test')
