"""cgs_nlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view, name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from SpiderAPI.views import SpiderWeibo
from ScrapydAPI.views import ScrapydWeibo
from SnowNLPAPI.views import SnowNLPWeibo



urlpatterns = [
    path('admin/', admin.site.urls),
    path('spiderapi/', SpiderWeibo.SpiderAPI, name="spiderapi"),
    path('tweetsapi/', SpiderWeibo.TweetsAPI, name="tweetsapi"),
    path('wordcloudapi/', SpiderWeibo.WordCloudAPI, name="wordcloudapi"),
    path('getweibo/', SpiderWeibo.getWeibo, name="getweibo"),
    path('getcomment/', SpiderWeibo.getComment, name="getcomment"),
    path('scrapydapi/', ScrapydWeibo.ScrapydAPI, name="scrapydapi"),
    path('cancelscrapyd/', ScrapydWeibo.CancelScrapyd, name="cancelscrapyd"),
    path('getlasted/', ScrapydWeibo.getLasted, name="getlasted"),
    path('getgroup/', ScrapydWeibo.getGroupInfo, name="getgroup"),
    path('snownlpapi/', SnowNLPWeibo.SnowNLPAPI, name="snownlpapi"),
    # 认证相关路由
    path('api/auth/register/', SpiderWeibo.auth_register, name="auth_register"),
    path('api/auth/login/', SpiderWeibo.auth_login, name="auth_login"),
    path('api/auth/logout/', SpiderWeibo.auth_logout, name="auth_logout"),
    path('api/auth/current/', SpiderWeibo.auth_current, name="auth_current"),
    # 搜索记录相关路由
    path('api/history/add/', SpiderWeibo.search_history_add, name='search_history_add'),
    path('api/history/list/', SpiderWeibo.search_history_list, name='search_history_list'),
    
    # 数据导出相关路由
    path('api/export/tweets/', SpiderWeibo.export_tweets_csv, name='export_tweets_csv'),
    path('api/export/user/', SpiderWeibo.export_user_info, name='export_user_info'),
    
    # 热度排名相关路由
    path('api/hot/', SpiderWeibo.hot_tweets, name='hot_tweets'),
    
    path('', TemplateView.as_view(template_name="index.html")),
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.views import serve
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or settings.BASE_DIR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
