from unittest import TestCase
from os import environ, system, path
from pprint import pp


class EnvTests(TestCase):
    def test_env(self):
        """
        Show the current environment

        debug: print environ
        """
        self.assertIn('PYTHON_VERSION', dict(environ))

        # Uncomment to show full environ in logs
        # pp(dict(environ))

    def test_media_dir(self):
        """
        Test if MEDIA_ROOT directory exists

        debug: ls -la MEDIA_ROOT
        """
        from ..settings.base import MEDIA_ROOT

        self.assertTrue(path.isdir(MEDIA_ROOT))

        # Uncomment to show media directory in logs
        # system('ls -la ' + MEDIA_ROOT)
