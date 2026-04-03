# -*- coding: utf-8 -*-

# Define your item pipelines here
import os
import sys
import django

# 初始化 Django 环境（从 scrapydserver/ 向外找两层到 WeiboNLP/，再定位到 wcl_nlp/）
_scrapydserver_dir = os.path.dirname(os.path.abspath('.'))
_wcl_nlp_dir = os.path.dirname(_scrapydserver_dir)
_weibo_nlp_dir = os.path.dirname(_wcl_nlp_dir)
sys.path.insert(0, _scrapydserver_dir)
sys.path.insert(0, _wcl_nlp_dir)
sys.path.insert(0, _weibo_nlp_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wcl_nlp.settings')
django.setup()

from datetime import datetime
from src.SpiderAPI.models import UserInfo, TweetsInfo, RelationshipsInfo, CommentInfo
from src.SnowNLPAPI.snownlp import SnowNLP


def save_to_django(item, spider):
    """根据 spider 类型将 item 写入 Django 数据库"""
    if isinstance(item, dict):
        item_dict = item
    else:
        item_dict = dict(item)

    if spider.name == 'weibo_spider':
        # 判断是哪种 item
        if 'tweets_num' in item_dict or 'nick_name' in item_dict:
            # InformationItem
            info, created = UserInfo.objects.get_or_create(
                _id=item_dict.get('_id'),
                defaults={
                    'nick_name': item_dict.get('nick_name', ''),
                    'gender': item_dict.get('gender', ''),
                    'province': item_dict.get('province', ''),
                    'city': item_dict.get('city', ''),
                    'brief_introduction': item_dict.get('brief_introduction', ''),
                    'birthday': item_dict.get('birthday'),
                    'constellation': item_dict.get('constellation', ''),
                    'sex_orientation': item_dict.get('sex_orientation', ''),
                    'sentiment': item_dict.get('sentiment', ''),
                    'vip_level': item_dict.get('vip_level', ''),
                    'authentication': item_dict.get('authentication', ''),
                    'labels': item_dict.get('labels', ''),
                    'tweets_num': item_dict.get('tweets_num', 0),
                    'follows_num': item_dict.get('follows_num', 0),
                    'fans_num': item_dict.get('fans_num', 0),
                    'Image': item_dict.get('Image', ''),
                    'crawl_time': item_dict.get('crawl_time', datetime.now()),
                }
            )
            if not created:
                for k, v in item_dict.items():
                    if hasattr(info, k) and k not in ('_id',):
                        setattr(info, k, v)
                info.save()

        elif 'weibo_url' in item_dict and 'content' in item_dict:
            # TweetsItem
            content = item_dict.get('content', '')
            if not content:
                return item
            try:
                info, _ = UserInfo.objects.get_or_create(_id=item_dict.get('user_id'))

                # 情感分析
                try:
                    s = SnowNLP(content)
                    sentiments = str(s.sentiments)
                    tags = ','.join(s.keywords(5))
                    pinyin = ''.join([p for w, p in s.tags])
                except Exception:
                    sentiments = '0.5'
                    tags = ''
                    pinyin = ''

                # 解析来源
                tools = ''
                created = item_dict.get('created_at', '')
                if '来自' in created:
                    parts = created.split('来自')
                    created = parts[0].strip()
                    tools = parts[1].strip() if len(parts) > 1 else ''

                tweet, created = TweetsInfo.objects.get_or_create(
                    _id=item_dict.get('_id'),
                    defaults={
                        'UserInfo': info,
                        'PubTime': created,
                        'Content': content,
                        'Like': item_dict.get('like_num', 0),
                        'Transfer': item_dict.get('repost_num', 0),
                        'Comment': item_dict.get('comment_num', 0),
                        'Tools': tools,
                        'sentiments': sentiments,
                        'tags': tags,
                        'pinyin': pinyin,
                        'crawl_time': item_dict.get('crawl_time', datetime.now()),
                    }
                )
            except Exception as e:
                spider.logger.warning(f"TweetsItem 保存失败: {e}")

        elif 'fan_id' in item_dict:
            # RelationshipsItem
            try:
                RelationshipsInfo.objects.get_or_create(
                    _id=item_dict.get('_id'),
                    defaults={
                        'fan_id': item_dict.get('fan_id', ''),
                        'followed_id': item_dict.get('followed_id', ''),
                        'crawl_time': item_dict.get('crawl_time', datetime.now()),
                    }
                )
            except Exception as e:
                spider.logger.warning(f"RelationshipsItem 保存失败: {e}")

        elif 'comment_user_id' in item_dict or 'content' in item_dict:
            # CommentItem
            try:
                CommentInfo.objects.get_or_create(
                    _id=item_dict.get('_id', ''),
                    defaults={
                        'CommentWeiboInfo_id': item_dict.get('weibo_url', ''),
                        'c_user_id': item_dict.get('comment_user_id', ''),
                        'c_text': item_dict.get('content', ''),
                        'c_created_at': item_dict.get('created_at', ''),
                        'crawl_time': item_dict.get('crawl_time', datetime.now()),
                    }
                )
            except Exception as e:
                spider.logger.warning(f"CommentItem 保存失败: {e}")

    return item


class BotPipeline:
    def process_item(self, item, spider):
        try:
            save_to_django(item, spider)
        except Exception as e:
            spider.logger.error(f"Pipeline 错误: {e}")
        return item
