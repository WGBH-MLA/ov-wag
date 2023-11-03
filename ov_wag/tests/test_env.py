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
