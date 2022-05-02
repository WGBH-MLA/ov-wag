from django.urls import reverse
from rest_framework import status
from unittest import TestCase
from rest_framework.test import APITestCase
from wagtail.core.models import Page, Site
import wagtail_factories
from exhibit.models import ExhibitPage, ExhibitPageApiSchema
from exhibit.tests.factories import ExhibitPageFactory


class ApiTests(APITestCase):
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

    def test_exhibit_cover_image(self):
        """
        GET /api/v2/pages/{id} for Exhibit pages

        Compare response against ExhibitSchema
        """
        exhibit_page = ExhibitPageFactory.create(parent=self.__home_page())
        response = self.client.get(f'/api/v2/pages/{exhibit_page.id}/', format='json')
        json = response.json()
        ExhibitPageApiSchema(**json)
        self.assertIsNotNone(json['cover_image']['meta']['download_url'])

    def __home_page(self):
        return Site.objects.filter(is_default_site=True).first().root_page
