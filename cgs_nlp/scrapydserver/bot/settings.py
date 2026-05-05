# -*- coding: utf-8 -*-
import sys
import os
import base64

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'cgs_nlp.settings'))

_scrapydserver_dir = os.path.dirname(os.path.abspath(__file__))
_cgs_nlp_dir = os.path.dirname(_scrapydserver_dir)
_weibo_nlp_dir = os.path.dirname(_cgs_nlp_dir)
sys.path.insert(0, _scrapydserver_dir)
sys.path.insert(0, _cgs_nlp_dir)
sys.path.insert(0, _weibo_nlp_dir)

import django
django.setup()

import random
from django.conf import settings

listCookie = []
try:
    from SpiderAPI.models import Target
    targets = Target.objects.all()
    for t in targets:
        cookie_val = t.get_cookie()
        if cookie_val:
            listCookie.append((cookie_val,))
    random.shuffle(listCookie)
except Exception as e:
    print(f"[Scrapyd] Cookie加载失败: {e}")
    listCookie = []

BOT_NAME = 'bot'
SPIDER_MODULES = ['bot.spiders']
NEWSPIDER_MODULE = 'bot.spiders'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'bot.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'bot.pipelines.BotPipeline': 300,
}

ROBOTSTXT_OBEY = False
