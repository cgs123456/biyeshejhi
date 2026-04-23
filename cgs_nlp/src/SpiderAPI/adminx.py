# -*- encoding: utf-8 -*-
"""
@FileName：adminx.py\n
@Description：\n
@Author：cgs\n
@Time：2022/4/11 16:03\n
@Department：毕业设计
@Copyright：cgs
"""
import xadmin
from xadmin import views
# here put the import lib
from .models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo, ImgInfo, UserProfile, SearchHistory


class TargetAdmin(object):
    list_display = ['uid', 'cookie_preview', 'add_time']
    search_fields = ['uid', 'cookie', 'add_time']
    list_filter = ['uid', 'cookie', 'add_time']
    
    def cookie_preview(self, obj):
        """Cookie 预览（只显示前 50 个字符）"""
        cookie = obj.get_cookie()
        if len(cookie) > 50:
            return cookie[:50] + "..."
        return cookie
    cookie_preview.short_description = 'Cookie（解密预览'


class UserInfoAdmin(object):
    list_display = ['_id', 'Image', 'NickName', 'Gender', 'Province', 'City', 'BriefIntroduction', 'Birthday',
                    'Constellation',
                    'Num_Tweets', 'Num_Follows', 'Num_Fans', 'SexOrientation', 'Sentiment', 'VIPlevel',
                    'Verified', 'URL']
    search_fields = ['_id', 'Image', 'NickName', 'Gender', 'Province', 'City', 'BriefIntroduction', 'Birthday',
                     'Constellation',
                     'Num_Tweets', 'Num_Follows', 'Num_Fans', 'SexOrientation', 'Sentiment', 'VIPlevel',
                     'Verified', 'URL']
    list_filter = ['_id', 'Image', 'NickName', 'Gender', 'Province', 'City', 'BriefIntroduction', 'Birthday',
                   'Constellation',
                   'Num_Tweets', 'Num_Follows', 'Num_Fans', 'SexOrientation', 'Sentiment', 'VIPlevel', 'Verified',
                   'URL']


class TweetsInfoAdmin(object):
    list_display = ['UserInfo', '_id', 'Content', 'PubTime', 'PubTools', 'Like', 'Comment', 'Transfer',
                    'tags', 'pinyin', 'sentiments']
    search_fields = ['UserInfo__NickName', '_id', 'Content', 'PubTime', 'PubTools', 'Like', 'Comment',
                     'Transfer', 'tags', 'pinyin', 'sentiments']
    list_filter = ['UserInfo', '_id', 'Content', 'PubTime', 'PubTools', 'Like', 'Comment', 'Transfer',
                   'tags', 'pinyin', 'sentiments']


class CommentWeiboInfoAdmin(object):
    list_display = ['wb_id', 'wb_userId', 'wb_userName', 'wb_user_profile_image_url', 'wb_created_at', 'wb_source',
                    'wb_text', 'wb_pic_ids', 'wb_repost_num', 'wb_comment_num', 'wb_like_num']
    search_fields = ['wb_id', 'wb_userId', 'wb_userName', 'wb_user_profile_image_url', 'wb_created_at', 'wb_source',
                     'wb_text', 'wb_pic_ids', 'wb_repost_num', 'wb_comment_num', 'wb_like_num']
    list_filter = ['wb_id', 'wb_userId', 'wb_userName', 'wb_user_profile_image_url', 'wb_created_at', 'wb_source',
                   'wb_text', 'wb_pic_ids', 'wb_repost_num', 'wb_comment_num', 'wb_like_num']


class CommentInfoAdmin(object):
    list_display = ['CommentWeiboInfo', 'c_id', 'c_created_at', 'c_source', 'c_text',
                    'c_like_num', 'c_userId', 'c_userName', 'c_user_profile_image_url', 'c_user_profile_url']
    search_fields = ['CommentWeiboInfo__wb_userName', 'c_id', 'c_created_at', 'c_source', 'c_text',
                     'c_like_num', 'c_userId', 'c_userName', 'c_user_profile_image_url', 'c_user_profile_url']
    list_filter = ['CommentWeiboInfo', 'c_id', 'c_created_at', 'c_source', 'c_text',
                   'c_like_num', 'c_userId', 'c_userName', 'c_user_profile_image_url', 'c_user_profile_url']


class ImgInfoAdmin(object):
    list_display = ['UserInfo', 'wordcloud']
    search_fields = ['UserInfo__NickName', 'wordcloud']
    list_filter = ['UserInfo', 'wordcloud']


class UserProfileAdmin(object):
    list_display = ['user', 'nickname', 'created_at', 'updated_at']
    search_fields = ['user__username', 'nickname']
    list_filter = ['created_at', 'updated_at']


class SearchHistoryAdmin(object):
    list_display = ['user', 'keyword', 'weibo_id', 'nickname', 'search_time']
    search_fields = ['user__username', 'keyword', 'weibo_id', 'nickname']
    list_filter = ['search_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = u"微博用户情感分析系统后台"
    site_footer = u"微博用户情感分析系统"
    menu_style = "accordion"


xadmin.site.register(Target, TargetAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(TweetsInfo, TweetsInfoAdmin)
xadmin.site.register(CommentWeiboInfo, CommentWeiboInfoAdmin)
xadmin.site.register(CommentInfo, CommentInfoAdmin)
xadmin.site.register(ImgInfo, ImgInfoAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(SearchHistory, SearchHistoryAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
