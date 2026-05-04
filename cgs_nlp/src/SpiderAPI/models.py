from django.db import models
from django.contrib.auth.models import User


class Target(models.Model):
    uid = models.CharField('uid', max_length=255, default='', db_index=True, unique=True)
    cookie = models.CharField('cookie', max_length=2048, default='')
    isScrapy = models.IntegerField('是否已爬取', default=0)
    group = models.IntegerField('用户分组', default=0)
    add_time = models.DateTimeField('add_time', auto_now_add=True, db_index=True)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_target'
        verbose_name = '爬取目标'
        verbose_name_plural = '爬取目标'

    def __str__(self):
        return self.uid
    
    def set_cookie(self, cookie_value):
        """设置加密的 cookie"""
        from SpiderAPI.crypto_utils import SimpleEncryption
        self.cookie = SimpleEncryption.encrypt(cookie_value)
    
    def get_cookie(self):
        """获取解密的 cookie"""
        from SpiderAPI.crypto_utils import SimpleEncryption
        return SimpleEncryption.decrypt(self.cookie)


class UserInfo(models.Model):
    _id = models.CharField('用户ID', max_length=50, primary_key=True)
    Image = models.CharField('头像地址', max_length=255)
    NickName = models.CharField('昵称', max_length=255, db_index=True)
    Gender = models.CharField('性别', max_length=10, default='')
    Province = models.CharField('省份', max_length=100, default='')
    City = models.CharField('城市', max_length=100, default='')
    Birthday = models.CharField('生日', max_length=50, default='')
    Constellation = models.CharField('星座', max_length=50, default='')
    Location = models.CharField('所在地', max_length=255, default='')
    URL = models.URLField('首页链接', max_length=255, default='')
    Num_Follows = models.IntegerField('关注数', default=0)
    Num_Fans = models.IntegerField('粉丝数', default=0)
    Num_Tweets = models.IntegerField('微博数', default=0)
    Education = models.CharField('教育信息', max_length=255, default='')
    Company = models.CharField('公司信息', max_length=255, default='')
    Tags = models.CharField('标签', max_length=255, default='')
    Description = models.CharField('简介', max_length=255, default='')
    BriefIntroduction = models.CharField('简价', max_length=500, default='')
    SexOrientation = models.CharField('性取向', max_length=50, default='')
    Sentiment = models.CharField('感情状况', max_length=50, default='')
    VIPlevel = models.CharField('会员等级', max_length=50, default='')
    Verified = models.BooleanField('是否认证', default=False)
    Verified_reason = models.CharField('认证原因', max_length=255, default='')
    verified_type = models.CharField('认证类型', max_length=10, default='')
    follow_me = models.BooleanField('是否关注我', default=False)
    following = models.BooleanField('是否正在关注', default=False)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_UserInfo'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.NickName


class TweetsInfo(models.Model):
    _id = models.CharField('微博ID', max_length=50, primary_key=True)
    Content = models.TextField('微博内容', default='')
    PubTime = models.DateTimeField('发布时间', null=True, blank=True, db_index=True)
    PubTools = models.CharField('发布工具', max_length=255, default='')
    Like = models.IntegerField('点赞数', default=0)
    Comment = models.IntegerField('评论数', default=0)
    Transfer = models.IntegerField('转发数', default=0)
    Image = models.TextField('图片地址', default='')
    UserInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='tweets', db_index=True)

    tags = models.CharField('标签', max_length=255, default='')
    pinyin = models.CharField('拼音', max_length=1024, default='')
    sentiments = models.CharField('情感分析', max_length=50, default='')

    class Meta:
        managed = True
        db_table = 'SpiderAPI_TweetsInfo'
        verbose_name = '微博信息'
        verbose_name_plural = '微博信息'
        ordering = ['-PubTime']

    def __str__(self):
        return self.Content[:50]


class CommentWeiboInfo(models.Model):
    wb_id = models.CharField('wb_id', max_length=255, unique=True, db_index=True)
    wb_userId = models.CharField('用户ID', max_length=255, default='', db_index=True)
    wb_userName = models.CharField('用户名', max_length=255, default='', db_index=True)
    wb_user_profile_image_url = models.URLField('用户头像', default='')
    wb_text = models.TextField('微博内容', default='')
    wb_created_at = models.DateTimeField('微博发布时间', null=True, blank=True, db_index=True)
    wb_source = models.CharField('来源', max_length=255, default='')
    wb_pic_ids = models.JSONField('图片ID列表', default=list, blank=True, null=True)
    wb_like_num = models.IntegerField('微博点赞数', default=0)
    wb_comment_num = models.IntegerField('微博评论数', default=0)
    wb_repost_num = models.IntegerField('微博转发数', default=0)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_CommentWeiboInfo'
        verbose_name = '微博评论信息'
        verbose_name_plural = '微博评论信息'

    def __str__(self):
        return self.wb_userName


class CommentInfo(models.Model):
    c_id = models.CharField('评论ID', max_length=50, primary_key=True)
    c_userId = models.CharField('用户ID', max_length=255, default='', db_index=True)
    c_userName = models.CharField('用户名', max_length=255, default='', db_index=True)
    c_user_profile_image_url = models.URLField('用户头像', default='')
    c_user_profile_url = models.URLField('用户首页', default='')
    c_source = models.CharField('来源', max_length=255, default='')
    c_text = models.TextField('评论内容', default='')
    c_created_at = models.DateTimeField('评论时间', null=True, blank=True, db_index=True)
    c_like_num = models.IntegerField('点赞数', default=0)
    c_sentiments = models.CharField('情感分析', max_length=50, default='')
    CommentWeiboInfo = models.ForeignKey(
        CommentWeiboInfo, on_delete=models.CASCADE,
        related_name='comments', db_index=True,
        to_field='wb_id'
    )

    class Meta:
        managed = True
        db_table = 'SpiderAPI_CommentInfo'
        verbose_name = '评论详情'
        verbose_name_plural = '评论详情'
        ordering = ['-c_like_num']

    def __str__(self):
        return self.c_text[:50]


class ImgInfo(models.Model):
    _id = models.BigAutoField(primary_key=True)
    UserInfo = models.OneToOneField(UserInfo, on_delete=models.CASCADE, related_name='img_info')
    wordcloud = models.JSONField('词云数据', default=dict)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_ImgInfo'
        verbose_name = '图片信息'
        verbose_name_plural = '图片信息'

    def __str__(self):
        return str(self.UserInfo)


class RelationshipsInfo(models.Model):
    _id = models.CharField('关系ID', max_length=100, primary_key=True)
    fan_id = models.CharField('关注者ID', max_length=50, db_index=True)
    followed_id = models.CharField('被关注者ID', max_length=50, db_index=True)
    crawl_time = models.DateTimeField('抓取时间', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_RelationshipsInfo'
        verbose_name = '用户关系'
        verbose_name_plural = '用户关系'

    def __str__(self):
        return f'{self.fan_id} -> {self.followed_id}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField('昵称', max_length=50, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_UserProfile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} - {self.nickname}'


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history', null=True, blank=True)
    keyword = models.CharField('搜索关键词', max_length=255)
    weibo_id = models.CharField('微博ID', max_length=50, default='')
    nickname = models.CharField('用户昵称', max_length=255, default='')
    search_time = models.DateTimeField('搜索时间', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'SpiderAPI_SearchHistory'
        verbose_name = '搜索记录'
        verbose_name_plural = '搜索记录'
        ordering = ['-search_time']

    def __str__(self):
        return f'{self.keyword} - {self.search_time.strftime("%Y-%m-%d %H:%M")}'
