from django.contrib import admin
from .models import (
    Target,
    UserInfo,
    TweetsInfo,
    CommentWeiboInfo,
    CommentInfo,
    ImgInfo,
    RelationshipsInfo,
    UserProfile,
    SearchHistory
)

# 添加所有模型！
admin.site.register(Target)
admin.site.register(UserInfo)
admin.site.register(TweetsInfo)
admin.site.register(CommentWeiboInfo)
admin.site.register(CommentInfo)
admin.site.register(ImgInfo)
admin.site.register(RelationshipsInfo)
admin.site.register(UserProfile)
admin.site.register(SearchHistory)
