from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from SpiderAPI.models import UserInfo, TweetsInfo


class SpiderAPITests(TestCase):
    """基础测试套件"""

    def setUp(self):
        """测试前准备数据"""
        # 创建测试用户
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_get_lasted_endpoint(self):
        """测试获取最新信息接口"""
        url = reverse('getlasted')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_hot_tweets_endpoint(self):
        """测试热门微博接口"""
        url = reverse('hot_tweets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_wordcloud_endpoint_get_without_param(self):
        """测试词云接口没有参数时"""
        url = reverse('wordcloudapi')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_export_tweets_requires_login(self):
        """测试导出接口需要登录"""
        url = reverse('export_tweets_csv')
        response = self.client.get(url)
        # 应该重定向到登录页或返回 403/302
        self.assertIn(response.status_code, [302, 403])

    def test_export_user_info_requires_login(self):
        """测试导出用户信息需要登录"""
        url = reverse('export_user_info')
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])


class AuthEndpointTests(TestCase):
    """认证相关接口测试"""

    def test_auth_current_unauthenticated(self):
        """测试未登录状态下的当前用户接口"""
        url = reverse('auth_current')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_auth_register_endpoint_exists(self):
        """测试注册接口存在"""
        url = reverse('auth_register')
        response = self.client.post(url, {})  # 空数据，应该返回错误但 404
        self.assertNotEqual(response.status_code, 404)
