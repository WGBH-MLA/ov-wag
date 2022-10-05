from rest_framework import status
from rest_framework.test import APITestCase
from wagtail.core.models import Site
import wagtail_factories
from exhibits.models import ExhibitPageApiSchema
from exhibits.tests.factories import ExhibitPageFactory


class ApiTests(APITestCase):
    def assertValidSchema(self, item):
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
        response = self.client.get(f'/api/v2/exhibits/{exhibit_page.id}/', format='json')
        json = response.json()
        self.assertValidSchema(json)

    def test_exhibit_api_schema_multiple(self):
        """
        GET /api/v2/exhibit for Exhibit pages

        Compare response against ExhibitSchema
        """
        exhibit_page = ExhibitPageFactory.create(parent=self.__home_page())
        response = self.client.get(f'/api/v2/exhibits/', format='json')
        json = response.json()
        for item in json['items']:
            self.assertValidSchema(item)

    def __home_page(self):
        return Site.objects.filter(is_default_site=True).first().root_page
