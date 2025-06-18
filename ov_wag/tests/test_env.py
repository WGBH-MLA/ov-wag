from os import environ as env
from os import path
from unittest import TestCase
from ov_wag.settings.base import MEDIA_ROOT


class EnvTests(TestCase):
    def test_media_dir(self):
        """
        Test if MEDIA_ROOT directory exists

        debug: ls -la MEDIA_ROOT
        """

        self.assertTrue(path.isdir(MEDIA_ROOT))

        # Uncomment to show media directory in logs

    def test_env(self):
        """Test if the environment variables are set"""

        self.assertTrue(env.get('DJANGO_SETTINGS_MODULE') == 'ov_wag.settings.test')
