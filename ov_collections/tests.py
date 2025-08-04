from django.test import TestCase

from ov_collections.factories import OpenVaultCollectionFactory
from ov_collections.models import OpenVaultCollection


# Create your tests here.
class ExhibitPageTests(TestCase):
    def test_exhibit_page_factory(self):
        """
        ExhibitPageFactory creates ExhibitPage model instances
        """
        self.assertIsInstance(OpenVaultCollectionFactory.create(), OpenVaultCollection)
