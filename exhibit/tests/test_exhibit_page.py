from django.test import TestCase
from ..models import *
from .factories import *

# Create your tests here.
class ExhibitPageTests(TestCase):
    def test_exhibit_page_factory(self):
        """
        ExhibitPageFactory creates ExhibitPage model instances
        """
        self.assertIsInstance(ExhibitPageFactory.create(), ExhibitPage)
