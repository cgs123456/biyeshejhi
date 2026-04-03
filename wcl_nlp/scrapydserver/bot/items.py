# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See: https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class TweetsItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    weibo_url = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field()
    like_num = scrapy.Field()
    repost_num = scrapy.Field()
    comment_num = scrapy.Field()
    crawl_time = scrapy.Field()
    tools = scrapy.Field()
    user_name = scrapy.Field()
    isTransfer = scrapy.Field()
    transfer_user = scrapy.Field()
    sentiments = scrapy.Field()
    tags = scrapy.Field()
    pinyin = scrapy.Field()


class InformationItem(scrapy.Item):
    _id = scrapy.Field()
    nick_name = scrapy.Field()
    gender = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    brief_introduction = scrapy.Field()
    birthday = scrapy.Field()
    constellation = scrapy.Field()
    sex_orientation = scrapy.Field()
    sentiment = scrapy.Field()
    vip_level = scrapy.Field()
    authentication = scrapy.Field()
    labels = scrapy.Field()
    tweets_num = scrapy.Field()
    follows_num = scrapy.Field()
    fans_num = scrapy.Field()
    Image = scrapy.Field()
    crawl_time = scrapy.Field()


class RelationshipsItem(scrapy.Item):
    _id = scrapy.Field()
    fan_id = scrapy.Field()
    followed_id = scrapy.Field()
    crawl_time = scrapy.Field()


class CommentItem(scrapy.Item):
    _id = scrapy.Field()
    weibo_url = scrapy.Field()
    comment_user_id = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field()
    crawl_time = scrapy.Field()
