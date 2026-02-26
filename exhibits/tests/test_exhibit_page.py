from django.test import TestCase
from ..models import OpenVaultExhibit
from .factories import ExhibitPageFactory


# Create your tests here.
class ExhibitPageTests(TestCase):
    def test_exhibit_page_factory(self):
        """
        ExhibitPageFactory creates ExhibitPage model instances
        """
        self.assertIsInstance(ExhibitPageFactory.create(), OpenVaultExhibit)
