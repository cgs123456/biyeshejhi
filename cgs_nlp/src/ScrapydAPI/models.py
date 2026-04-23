
# ScrapydAPI 不再定义独立的模型
# 直接使用 SpiderAPI 中完整的模型定义
# 请从 SpiderAPI.models 导入 Target, UserInfo, TweetsInfo 等模型

# 如果需要在 admin 中显示，可以导入并注册：
# from SpiderAPI.models import Target, UserInfo, TweetsInfo
# from django.contrib import admin
# admin.site.register(Target)
# admin.site.register(UserInfo)
# admin.site.register(TweetsInfo)

