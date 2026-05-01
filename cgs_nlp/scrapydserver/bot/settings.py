# -*- coding: utf-8 -*-
import sys
import os
import base64

os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 'cgs_nlp.settings')

scrapydserver_dir = os.path.dirname(os.path.abspath('.'))
cgs_nlp_dir = os.path.dirname(scrapydserver_dir)
sys.path.insert(0, scrapydserver_dir)
sys.path.insert(0, cgs_nlp_dir)

import django
django.setup()

import random
import pymysql.cursors
from cryptography.fernet import Fernet
from django.conf import settings

def get_crypto_key():
    """获取加密密钥（与 Django 侧保持一致）"""
    secret_key = settings.SECRET_KEY
    key_bytes = secret_key.encode('utf-8')
    key_bytes = key_bytes[:32].ljust(32, b'0')
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    return fernet_key

def decrypt_cookie(encrypted_text):
    """解密 cookie"""
    try:
        if not encrypted_text:
            return encrypted_text
        
        key = get_crypto_key()
        f = Fernet(key)
        decoded = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
        decrypted = f.decrypt(decoded)
        return decrypted.decode('utf-8')
    except Exception:
        return encrypted_text

listCookie = []
db_password = os.environ.get('DB_PASSWORD', '')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', 3306))
db_name = os.environ.get('DB_NAME', 'weibo_nlp')
db_user = os.environ.get('DB_USER', 'root')

if db_password:
    try:
        connect = pymysql.connect(
            host=db_host,
            port=db_port,
            db=db_name,
            user=db_user,
            passwd=db_password,
            charset='utf8mb4',
            use_unicode=True)
        cursor = connect.cursor()
        cursor.execute("""SELECT cookie from scrapydapi_target""")
        cookie = cursor.fetchall()
        connect.close()
        cursor.close()
        for res1 in cookie:
            # 解密 cookie
            decrypted = decrypt_cookie(res1[0]) if res1 and res1[0] else ''
            listCookie.append((decrypted,))
        random.shuffle(listCookie)
    except Exception as e:
        print(f"[Scrapyd] MySQL连接失败，使用默认Cookie: {e}")
        listCookie = []
else:
    print(f"[Scrapyd] 未配置数据库密码，使用默认Cookie")

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
