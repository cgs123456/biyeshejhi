from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from SpiderAPI.models import UserInfo, TweetsInfo


class SpiderAPITests(TestCase):
    """基础测试套件"""

    def setUp(self):
        """测试前准备数据"""
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
        """测试词云接口没有参数时返回400"""
        url = reverse('wordcloudapi')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_export_tweets_requires_login(self):
        """测试导出接口需要登录"""
        url = reverse('export_tweets_csv')
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_export_user_info_requires_login(self):
        """测试导出用户信息需要登录"""
        url = reverse('export_user_info')
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_export_tweets_after_login(self):
        """测试登录后导出接口可访问"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('export_tweets_csv')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])

    def test_export_user_info_after_login(self):
        """测试登录后导出用户信息可访问"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('export_user_info')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])

    def test_spider_api_invalid_weibo_id(self):
        """测试爬虫接口无效微博ID"""
        url = reverse('spiderapi')
        response = self.client.post(url, {'weiboId': 'abc'})
        self.assertEqual(response.status_code, 400)

    def test_spider_api_empty_weibo_id(self):
        """测试爬虫接口空微博ID"""
        url = reverse('spiderapi')
        response = self.client.post(url, {'weiboId': ''})
        self.assertEqual(response.status_code, 400)

    def test_wordcloud_nonexistent_user(self):
        """测试词云接口不存在的用户返回404"""
        url = reverse('wordcloudapi')
        response = self.client.get(url, {'weiboId': '9999999999'})
        self.assertEqual(response.status_code, 404)


class AuthEndpointTests(TestCase):
    """认证相关接口测试"""

    def test_auth_current_unauthenticated(self):
        """测试未登录状态下的当前用户接口"""
        url = reverse('auth_current')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('isLoggedIn', True))

    def test_auth_register_endpoint_exists(self):
        """测试注册接口存在"""
        url = reverse('auth_register')
        response = self.client.post(url, content_type='application/json', data={})
        self.assertNotEqual(response.status_code, 404)

    def test_auth_register_weak_password(self):
        """测试弱密码注册被拒绝"""
        url = reverse('auth_register')
        response = self.client.post(url, content_type='application/json', data={
            'username': 'weakpwuser',
            'password': '1'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('success', True))

    def test_auth_register_valid(self):
        """测试正常注册"""
        url = reverse('auth_register')
        response = self.client.post(url, content_type='application/json', data={
            'username': 'validuser',
            'password': 'validpass123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success', False))

    def test_auth_login_valid(self):
        """测试正常登录"""
        User.objects.create_user(username='loginuser', password='loginpass123')
        url = reverse('auth_login')
        response = self.client.post(url, content_type='application/json', data={
            'username': 'loginuser',
            'password': 'loginpass123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success', False))

    def test_auth_login_wrong_password(self):
        """测试错误密码登录"""
        User.objects.create_user(username='wrongpwuser', password='correctpass123')
        url = reverse('auth_login')
        response = self.client.post(url, content_type='application/json', data={
            'username': 'wrongpwuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('success', True))


class ScrapydAPITests(TestCase):
    """Scrapyd相关接口测试"""

    def test_get_lasted_endpoint(self):
        """测试获取最新信息接口"""
        url = reverse('getlasted')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_group_info_endpoint_get(self):
        """测试群组信息接口"""
        url = reverse('getgroup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_scrapyd_endpoint_accessible(self):
        """测试Scrapyd接口可访问（不需要登录）"""
        url = reverse('scrapydapi')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 503])


class SnowNLPAPITests(TestCase):
    """SnowNLP相关接口测试"""

    def test_snownlp_endpoint(self):
        """测试SnowNLP接口"""
        url = reverse('snownlpapi')
        response = self.client.get(url, {'snownlp': '今天天气真好'})
        self.assertEqual(response.status_code, 200)

    def test_snownlp_xss_protection(self):
        """测试SnowNLP接口XSS防护"""
        url = reverse('snownlpapi')
        response = self.client.get(url, {'snownlp': '<script>alert(1)</script>'})
        self.assertEqual(response.status_code, 200)
        import json
        data = json.loads(response.content)
        content = json.dumps(data)
        self.assertNotIn('<script>', content)
