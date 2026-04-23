from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ScrapydAPITests(TestCase):
    """Scrapyd API 基础测试套件"""

    def setUp(self):
        """测试前准备数据"""
        # 创建测试用户
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_get_lasted_endpoint(self):
        """测试获取最新信息接口"""
        url = reverse('getlasted')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_scrapyd_endpoint_requires_login(self):
        """测试 Scrapyd API 需要登录"""
        url = reverse('scrapydapi')
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_cancel_scrapyd_requires_login(self):
        """测试取消任务需要登录"""
        url = reverse('cancelscrapyd')
        response = self.client.post(url, {})
        self.assertIn(response.status_code, [302, 403])

    def test_group_info_endpoint_get(self):
        """测试群组信息接口（GET）"""
        url = reverse('getgroup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
