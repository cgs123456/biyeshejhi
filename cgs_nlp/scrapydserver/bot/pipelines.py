# -*- coding: utf-8 -*-

import os
import sys
import django

_pipeline_file = os.path.abspath(__file__)
_bot_dir = os.path.dirname(_pipeline_file)
_scrapydserver_dir = os.path.dirname(_bot_dir)
_cgs_nlp_dir = os.path.dirname(_scrapydserver_dir)
_weibo_nlp_dir = os.path.dirname(_cgs_nlp_dir)
sys.path.insert(0, _scrapydserver_dir)
sys.path.insert(0, _cgs_nlp_dir)
sys.path.insert(0, _weibo_nlp_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cgs_nlp.settings')
django.setup()

from datetime import datetime
from SpiderAPI.models import UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo
from SnowNLPAPI.snownlp import SnowNLP


def save_to_django(item, spider):
    if isinstance(item, dict):
        item_dict = item
    else:
        item_dict = dict(item)

    if spider.name == 'weibo_spider':
        if 'tweets_num' in item_dict or 'nick_name' in item_dict:
            info, created = UserInfo.objects.get_or_create(
                _id=item_dict.get('_id'),
                defaults={
                    'NickName': item_dict.get('nick_name', ''),
                    'Gender': item_dict.get('gender', ''),
                    'Province': item_dict.get('province', ''),
                    'City': item_dict.get('city', ''),
                    'BriefIntroduction': item_dict.get('brief_introduction', ''),
                    'Birthday': item_dict.get('birthday', ''),
                    'Constellation': item_dict.get('constellation', ''),
                    'SexOrientation': item_dict.get('sex_orientation', ''),
                    'Sentiment': item_dict.get('sentiment', ''),
                    'VIPlevel': item_dict.get('vip_level', ''),
                    'Verified_reason': item_dict.get('authentication', ''),
                    'Tags': item_dict.get('labels', ''),
                    'Num_Tweets': item_dict.get('tweets_num', 0),
                    'Num_Follows': item_dict.get('follows_num', 0),
                    'Num_Fans': item_dict.get('fans_num', 0),
                    'Image': item_dict.get('Image', ''),
                }
            )
            if not created:
                field_map = {
                    'nick_name': 'NickName', 'gender': 'Gender',
                    'province': 'Province', 'city': 'City',
                    'brief_introduction': 'BriefIntroduction',
                    'birthday': 'Birthday', 'constellation': 'Constellation',
                    'sex_orientation': 'SexOrientation', 'sentiment': 'Sentiment',
                    'vip_level': 'VIPlevel', 'authentication': 'Verified_reason',
                    'labels': 'Tags', 'tweets_num': 'Num_Tweets',
                    'follows_num': 'Num_Follows', 'fans_num': 'Num_Fans',
                    'Image': 'Image',
                }
                for src_key, dst_key in field_map.items():
                    if src_key in item_dict and item_dict[src_key]:
                        setattr(info, dst_key, item_dict[src_key])
                info.save()

        elif 'weibo_url' in item_dict and 'content' in item_dict:
            content = item_dict.get('content', '')
            if not content:
                return item
            try:
                info, _ = UserInfo.objects.get_or_create(_id=item_dict.get('user_id'))

                try:
                    s = SnowNLP(content)
                    sentiments = str(s.sentiments)
                    tags = ','.join(s.keywords(5))
                    pinyin = ''.join([p for w, p in s.tags])
                except Exception:
                    sentiments = '0.5'
                    tags = ''
                    pinyin = ''

                tools = ''
                created_at = item_dict.get('created_at', '')
                if isinstance(created_at, str) and '来自' in created_at:
                    parts = created_at.split('来自')
                    created_at = parts[0].strip()
                    tools = parts[1].strip() if len(parts) > 1 else ''

                tweet, created = TweetsInfo.objects.get_or_create(
                    _id=item_dict.get('_id'),
                    defaults={
                        'UserInfo': info,
                        'PubTime': created_at,
                        'Content': content,
                        'Like': item_dict.get('like_num', 0),
                        'Transfer': item_dict.get('repost_num', 0),
                        'Comment': item_dict.get('comment_num', 0),
                        'PubTools': tools,
                        'sentiments': sentiments,
                        'tags': tags,
                        'pinyin': pinyin,
                    }
                )
            except Exception as e:
                spider.logger.warning(f"TweetsItem save failed: {e}")

        elif 'comment_user_id' in item_dict:
            try:
                weibo_url = item_dict.get('weibo_url', '')
                if weibo_url:
                    wb_info, _ = CommentWeiboInfo.objects.get_or_create(
                        wb_id=weibo_url,
                        defaults={'wb_userId': '', 'wb_userName': '', 'wb_text': ''}
                    )
                    CommentInfo.objects.get_or_create(
                        c_id=item_dict.get('_id', ''),
                        defaults={
                            'CommentWeiboInfo': wb_info,
                            'c_userId': item_dict.get('comment_user_id', ''),
                            'c_text': item_dict.get('content', ''),
                            'c_created_at': item_dict.get('created_at', ''),
                        }
                    )
            except Exception as e:
                spider.logger.warning(f"CommentItem save failed: {e}")

    return item


class BotPipeline:
    def process_item(self, item, spider):
        try:
            save_to_django(item, spider)
        except Exception as e:
            spider.logger.error(f"Pipeline error: {e}")
        return item
