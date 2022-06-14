from unittest import TestCase
from os import environ
from pprint import pp

class EnvTests(TestCase):
    def test_env(self):
        """
        Show the current environment
        """
        pp(dict(environ))
