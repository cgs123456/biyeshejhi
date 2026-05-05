from django.test import TestCase
from django.urls import reverse
import json


class SnowNLPAPITests(TestCase):
    def test_snownlp_endpoint(self):
        url = reverse('snownlpapi')
        response = self.client.get(url, {'snownlp': '今天天气真好'})
        self.assertEqual(response.status_code, 200)

    def test_snownlp_returns_sentiments(self):
        url = reverse('snownlpapi')
        response = self.client.get(url, {'snownlp': '这个产品非常好用'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('sentiments', data)
        self.assertIsInstance(data['sentiments'], float)

    def test_snownlp_xss_protection(self):
        url = reverse('snownlpapi')
        response = self.client.get(url, {'snownlp': '<script>alert(1)</script>'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        content = json.dumps(data)
        self.assertNotIn('<script>', content)
