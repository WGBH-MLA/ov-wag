from rest_framework import status
from rest_framework.test import APITestCase


class HealthTests(APITestCase):
    def test_health(self):
        """
        GET /health
        """
        response = self.client.get('/api/v2/health/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'ok'})
