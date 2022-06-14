from unittest import TestCase
from os import environ, system
from pprint import pp

class EnvTests(TestCase):
    def test_env(self):
        """
        Show the current environment
        """
        pp(dict(environ))

    def test_show_media_dir(self):
        """
        ls -la /app/media
        """
        system('ls -la /app/media')
