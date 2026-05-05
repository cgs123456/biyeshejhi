from django.test import TestCase
from django.urls import reverse


class ScrapydAPITests(TestCase):
    def test_get_lasted_endpoint(self):
        url = reverse('getlasted')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_group_info_endpoint_get(self):
        url = reverse('getgroup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_scrapyd_endpoint_accessible(self):
        url = reverse('scrapydapi')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 503])
