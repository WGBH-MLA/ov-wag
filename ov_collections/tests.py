from django.test import TestCase

from ov_collections.factories import CollectionPageFactory
from ov_collections.models import Collection


# Create your tests here.
class ExhibitPageTests(TestCase):
    def test_exhibit_page_factory(self):
        """
        ExhibitPageFactory creates ExhibitPage model instances
        """
        self.assertIsInstance(CollectionPageFactory.create(), Collection)
