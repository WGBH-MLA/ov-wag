import wagtail_factories
from rest_framework import status
from rest_framework.test import APITestCase
from wagtail.models import Site

from exhibits.models import ExhibitPageApiSchema, ExhibitsApiSchema
from exhibits.tests.factories import ExhibitPageFactory
from aapb_exhibits.tests.factories import AAPBExhibitPageFactory


class ApiTests(APITestCase):
    def assert_valid_schema(self, item):
        ExhibitPageApiSchema(**item)
        return True

    def test_get_pages(self):
        """
        GET /api/v2/pages
        """
        response = self.client.get('/api/v2/pages/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_page(self):
        """
        GET /api/v2/pages/{id}
        """
        page = wagtail_factories.PageFactory.create(parent=self.__home_page())
        response = self.client.get(f'/api/v2/pages/{page.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_exhibit_page(self):
        """
        GET /api/v2/pages/{id} for Exhibit pages
        """
        exhibit_page = ExhibitPageFactory.create(parent=self.__home_page())
        response = self.client.get(f'/api/v2/pages/{exhibit_page.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exhibit_api_schema_single(self):
        """
        GET /api/v2/exhibit/{id} for Exhibit pages

        Compare response against ExhibitSchema
        """
        exhibit_page = ExhibitPageFactory.create(parent=self.__home_page())
        response = self.client.get(
            f'/api/v2/exhibits/{exhibit_page.id}/', format='json'
        )
        json = response.json()
        self.assert_valid_schema(json)

    def test_exhibit_api_schema_multiple(self):
        """
        GET /api/v2/exhibit for Exhibit pages

        Compare response against ExhibitsAPISchema
        """
        ExhibitPageFactory.create(parent=self.__home_page())
        response = self.client.get('/api/v2/exhibits/', format='json')
        json = response.json()
        for item in json['items']:
            assert ExhibitsApiSchema(**item)

    def test_exhibits_listing_defaults_to_open_vault(self):
        """
        GET /api/v2/exhibits returns only OpenVaultExhibit pages by default
        """
        ov_exhibit = ExhibitPageFactory.create(
            parent=self.__home_page(), title='OV Exhibit', slug='ov-exhibit'
        )
        AAPBExhibitPageFactory.create(
            parent=self.__home_page(), title='AAPB Exhibit', slug='aapb-exhibit'
        )
        response = self.client.get('/api/v2/exhibits/', format='json')
        ids = [item['id'] for item in response.json()['items']]
        self.assertIn(ov_exhibit.id, ids)
        self.assertEqual(len(ids), 1)

    def test_exhibits_listing_aapb_site(self):
        """
        GET /api/v2/exhibits on the aapb host returns only AAPBExhibit pages
        """
        ov_exhibit = ExhibitPageFactory.create(
            parent=self.__home_page(), title='OV Exhibit', slug='ov-exhibit'
        )
        aapb_exhibit = AAPBExhibitPageFactory.create(
            parent=self.__home_page(), title='AAPB Exhibit', slug='aapb-exhibit'
        )
        response = self.client.get(
            '/api/v2/exhibits/', format='json', HTTP_HOST='aapb.example.com'
        )
        ids = [item['id'] for item in response.json()['items']]
        self.assertIn(aapb_exhibit.id, ids)
        self.assertNotIn(ov_exhibit.id, ids)

    def __home_page(self):
        return Site.objects.filter(is_default_site=True).first().root_page
