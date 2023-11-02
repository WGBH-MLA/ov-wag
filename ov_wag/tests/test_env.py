from unittest import TestCase
from os import environ, path


class EnvTests(TestCase):
    def test_media_dir(self):
        """
        Test if MEDIA_ROOT directory exists

        debug: ls -la MEDIA_ROOT
        """
        from ..settings.base import MEDIA_ROOT

        self.assertTrue(path.isdir(MEDIA_ROOT))

        # Uncomment to show media directory in logs
        # system('ls -la ' + MEDIA_ROOT)
