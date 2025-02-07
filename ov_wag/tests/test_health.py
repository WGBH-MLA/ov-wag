from rest_framework import status
from rest_framework.test import APITestCase


class HealthTests(APITestCase):
    def test_health_status(self):
        """
        GET /api/v2/health/
        """
        response = self.client.get('/api/v2/health/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_response(self):
        """
        Ensure the health response contains the correct structure.
        """
        response = self.client.get('/api/v2/health/', format='json')
        self.assertTrue('status' in response.data)
        self.assertEqual(response.data['status'], 'ok')
