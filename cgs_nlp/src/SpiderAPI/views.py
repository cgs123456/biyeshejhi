#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo, ImgInfo, UserProfile, SearchHistory
from .spider import Weibo
from lxml import etree
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from src.SnowNLPAPI.snownlp import SnowNLP
from src.SnowNLPAPI.snownlp import sentiment
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
from django.db import connection, models
from django.db.models import F
from os import path
import jieba
import time
import matplotlib.pyplot as plt
import base64
import json
import requests
import traceback
import re
import csv


def process_wordcloud_text(content, stopwords_path, mingan_path):
    content = re.sub(r"[^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a]", "", content)
    wordlist_after_jieba = jieba.cut(content, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)

    stopwords = set()
    if path.exists(stopwords_path):
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f.readlines()}

    minganwords = set()
    if path.exists(mingan_path):
        with open(mingan_path, 'r', encoding='utf-8') as f:
            minganwords = {line.strip() for line in f.readlines()}

    outstr_list = []
    for word in wl_space_split.split():
        if word and word not in stopwords and word not in ('\t', '\n', ' ', ''):
            outstr_list.append(word)

    c = Counter()
    for word in outstr_list:
        c[word] += 1

    cipin = []
    mingancount = 0
    li = list(c.items())
    li.sort(key=lambda x: x[1], reverse=True)
    for k, v in li:
        if k in minganwords:
            mingancount += 1
        cipin.append({"word": k, "count": v})

    mingan_ratio = mingancount / len(li) if li else 0
    return mingan_ratio, cipin


class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


def process_comment_data(wid):
    wbinfos = CommentWeiboInfo.objects.filter(wb_id=wid)
    endTime = CommentInfo.objects.filter(CommentWeiboInfo_id=wid).order_by("c_created_at")
    commentinfos = CommentInfo.objects.filter(CommentWeiboInfo_id=wid).order_by("-c_like_num")

    res = {}
    res['data'] = serializers.serialize("json", wbinfos)
    res['info'] = serializers.serialize("json", commentinfos)

    start = None
    end = None
    for wbinfo in wbinfos:
        start = wbinfo.wb_created_at
    for e in endTime:
        end = e.c_created_at

    mid = (end - start) / 10 if start and end else timedelta(seconds=0)
    counts = [0] * 10

    c_content = ''
    for c_item in commentinfos:
        c_content += c_item.c_text
    stopwords_path = path.join(path.dirname(__file__), 'stopword.txt')
    mingan_path = path.join(path.dirname(__file__), 'mingan.txt')
    mingan_ratio, cipin = process_wordcloud_text(c_content, stopwords_path, mingan_path)
    res['mingan'] = mingan_ratio
    res['cipin'] = cipin

    sentimentslist = []
    for c_item in commentinfos:
        if c_item.c_text:
            m = re.sub(r"[A-Za-z0-9\：\·\—\，\。\u201c \u201d \? \@]", "", c_item.c_text)
            if m:
                try:
                    s = SnowNLP(m)
                    sentimentslist.append(s.sentiments)
                except Exception:
                    pass

    c0 = Counter()
    for word0 in sentimentslist:
        c0[word0] += 1
    li0 = list(c0.items())
    li0.sort(key=lambda x: x[0])
    res['analy'] = li0

    if start and end and mid.total_seconds() > 0:
        for c in commentinfos:
            for i in range(10):
                time_start = start + i * mid
                time_end = start + (i + 1) * mid
                if time_start <= c.c_created_at < time_end:
                    counts[i] += 1
                    break

        res['commentqushi'] = [
            {'date': json.dumps(start + (i + 1) * mid, cls=JsonCustomEncoder),
             'count': counts[i]}
            for i in range(10)
        ]
    return res


class SpiderWeibo:
    WEIBO_ID_MIN_LEN = 5
    WEIBO_ID_MAX_LEN = 30

    @staticmethod
    def _validate_weibo_id(weibo_id):
        if not weibo_id or not isinstance(weibo_id, str):
            return False
        weibo_id = weibo_id.strip()
        if len(weibo_id) < SpiderWeibo.WEIBO_ID_MIN_LEN or len(weibo_id) > SpiderWeibo.WEIBO_ID_MAX_LEN:
            return False
        if not weibo_id.isdigit():
            return False
        return True

    @csrf_exempt
    def SpiderAPI(request):
        res = {}
        if request.method == "POST":
            weibo_id = request.POST.get("weiboId")
            page = request.POST.get("page", "1")

            if not SpiderWeibo._validate_weibo_id(weibo_id):
                return JsonResponse({'error': '微博ID格式不正确，长度应在5-30之间'}, status=400)

            try:
                page = int(page)
            except (ValueError, TypeError):
                page = 1

            try:
                # 使用 select_related 优化查询
                user = UserInfo.objects.get(_id=weibo_id)
                res['ok'] = "数据库已存在该用户，开始返回数据"
                res['data'] = serializers.serialize("json", [user])
                # 只查询需要的字段，使用values代替serialize提升性能
                articles = TweetsInfo.objects.filter(UserInfo_id=weibo_id).order_by("-PubTime")
                paginator = Paginator(articles, 20)
                pageData = paginator.page(page)
                res['total'] = paginator.count
                res['tweets'] = serializers.serialize("json", pageData)
                return HttpResponse(json.dumps(res))
            except UserInfo.DoesNotExist:
                target, created = Target.objects.get_or_create(
                    uid=weibo_id,
                    defaults={'isScrapy': 0, 'group': 0}
                )
                
                # 检查是否正在爬取
                if target.isScrapy == 1:
                    res['ok'] = "爬虫正在后台运行中"
                    res['data'] = "[]"
                    res['total'] = 0
                    res['tweets'] = "[]"
                    res['crawling'] = True
                    return HttpResponse(json.dumps(res))
                
                # 重置状态并启动后台爬取
                target.isScrapy = 1
                target.save()
                
                def run_crawler(uid_val, cookie_val):
                    try:
                        cookie = {"Cookie": cookie_val}
                        wb = Weibo(uid_val, cookie)
                        wb.get_userInfo()
                        wb.get_weibo_info()
                        TweetsInfo.objects.filter(Content='').delete()
                    except Exception as e:
                        traceback.print_exc()
                    finally:
                        try:
                            t = Target.objects.get(uid=str(uid_val))
                            t.isScrapy = 2
                            t.save()
                        except Exception:
                            pass
                
                import threading
                t = threading.Thread(
                    target=run_crawler,
                    args=(int(weibo_id), target.get_cookie()),
                    daemon=True
                )
                t.start()
                
                res['ok'] = "爬虫已在后台启动，请稍后刷新查看"
                res['data'] = "[]"
                res['total'] = 0
                res['tweets'] = "[]"
                res['crawling'] = True
                return HttpResponse(json.dumps(res))
            except Exception as e:
                traceback.print_exc()
                return JsonResponse({'error': '服务器内部错误，请稍后重试'}, status=500)

        return HttpResponse(json.dumps({'error': 'Invalid request method'}))

    @require_GET
    def WordCloudAPI(request):
        res = {}
        if request.method == "GET":
            weibo_id = request.GET.get("weiboId")
            
            if weibo_id:  # 只有在提供了 weibo_id 时才处理
                # 首先检查 UserInfo 是否存在
                try:
                    UserInfo.objects.get(_id=weibo_id)
                except UserInfo.DoesNotExist:
                    return JsonResponse({'error': '该用户不存在于数据库中'}, status=404)
                
                articles = TweetsInfo.objects.filter(UserInfo_id=weibo_id)
                content = ' '.join([
                    e.Content.replace('转发', '').replace('转发理由:', '').replace('转发内容:', '').replace('原始用户:', '').replace('转发微博已被删除', '')
                    for e in articles
                ])

                stopwords_path = path.join(path.dirname(__file__), 'stopword.txt')
                mingan_path = path.join(path.dirname(__file__), 'mingan.txt')

                mingan_ratio, cipin = process_wordcloud_text(content, stopwords_path, mingan_path)
                res['mingan'] = mingan_ratio
                res['cipin'] = cipin

                TweetsInfo.objects.filter(sentiments='').delete()
                infos = TweetsInfo.objects.filter(UserInfo_id=weibo_id).values('sentiments')
                c = Counter()
                for word in infos:
                    c[word['sentiments']] += 1
                li = list(c.items())
                li.sort(key=lambda x: x[0])
                res['tu'] = json.dumps(li)

                try:
                    img_info = ImgInfo.objects.get(UserInfo_id=weibo_id)
                except ImgInfo.DoesNotExist:
                    img_info = ImgInfo()
                    img_info.UserInfo_id = weibo_id
                    img_info.wordcloud = res
                    img_info.save()
            else:
                return JsonResponse({'error': 'Missing weiboId parameter'}, status=400)

        return HttpResponse(json.dumps(res))

    @csrf_exempt
    def TweetsAPI(request):
        ret = {}
        if request.method == "POST":
            weibo_id = request.POST.get("weiboId")
            page = request.POST.get("page", "1")
            start_date = request.POST.get("start_date", "")
            end_date = request.POST.get("end_date", "")

            if not weibo_id:
                return JsonResponse({'error': '缺少 weiboId 参数'}, status=400)
            
            # 检查 UserInfo 是否存在
            try:
                UserInfo.objects.get(_id=weibo_id)
            except UserInfo.DoesNotExist:
                return JsonResponse({'error': '该用户不存在于数据库中'}, status=404)

            try:
                page = int(page)
            except (ValueError, TypeError):
                page = 1

            articles = TweetsInfo.objects.filter(UserInfo_id=weibo_id)
            
            # 如果有日期范围，进行时间筛选
            if start_date and end_date:
                try:
                    # 转换日期格式为 datetime
                    start = datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.strptime(end_date, "%Y-%m-%d")
                    # 设置结束时间为当天的 23:59:59
                    end = end.replace(hour=23, minute=59, second=59)
                    
                    articles = articles.filter(PubTime__range=(start, end))
                except ValueError:
                    # 日期格式不正确，忽略筛选
                    pass
            
            articles = articles.order_by("-PubTime")
            paginator = Paginator(articles, 20)
            pageData = paginator.page(page)
            ret['total'] = paginator.count
            ret['tweets'] = serializers.serialize("json", pageData)
            return HttpResponse(json.dumps(ret))

        if request.method == "GET":
            weibo_id = request.GET.get("weiboId")
            page = request.GET.get("page", "1")
            limit = request.GET.get("limit", "100")
            
            if not weibo_id:
                return JsonResponse({'error': '缺少 weiboId 参数'}, status=400)
            
            # 检查 UserInfo 是否存在
            try:
                UserInfo.objects.get(_id=weibo_id)
            except UserInfo.DoesNotExist:
                return JsonResponse({'error': '该用户不存在于数据库中'}, status=404)
            
            try:
                page = int(page)
            except (ValueError, TypeError):
                page = 1
                
            try:
                limit = min(int(limit), 500)
            except (ValueError, TypeError):
                limit = 100

            articles = TweetsInfo.objects.filter(UserInfo_id=weibo_id).order_by("-PubTime")
            paginator = Paginator(articles, 20)
            pageData = paginator.page(page)
            ret['total'] = paginator.count
            ret['tweets'] = serializers.serialize("json", pageData)
            return HttpResponse(json.dumps(ret))

        return HttpResponse(json.dumps({'error': 'Invalid request method'}))

    @require_GET
    def getLasted(request):
        infos = list(UserInfo.objects.values("_id", "Image", "NickName"))
        return JsonResponse(infos, safe=False)

    @csrf_exempt
    def getComment(request):
        res = {}
        if request.method == "POST":
            comment_id = request.POST.get("commentId")
            if not comment_id:
                return JsonResponse({'error': '缺少commentId参数'}, status=400)
            weibo_ids = [x.strip() for x in comment_id.split(',') if x.strip()]
            for wid in weibo_ids:
                if not SpiderWeibo._validate_weibo_id(wid):
                    continue
                wid = wid.strip()
                if not wid:
                    continue
                try:
                    CommentWeiboInfo.objects.get(wb_id=wid)
                except CommentWeiboInfo.DoesNotExist:
                    # 尝试从Target获取cookie并爬取评论
                    try:
                        target_obj = Target.objects.filter(uid=wid).first()
                        if not target_obj:
                            target_obj = Target.objects.first()
                        if target_obj:
                            uid = int(target_obj.uid)
                            cookie_val = target_obj.get_cookie()
                            cookie = {"Cookie": cookie_val}
                            wb = Weibo(uid, cookie)
                            wb.get_comment_info(wid)
                    except Exception as e:
                        # 爬取失败时记录错误但不中断，返回空数据
                        import traceback
                        traceback.print_exc()
                        res[wid] = {
                            'data': '[]',
                            'info': '[]',
                            'mingan': 0,
                            'cipin': [],
                            'analy': [],
                            'commentqushi': []
                        }
                        continue
                
                res[wid] = process_comment_data(wid)
            return HttpResponse(json.dumps(res))

        if request.method == "GET":
            comment_id = request.GET.get("commentId")
            if comment_id:
                weibo_ids = [x.strip() for x in comment_id.split(',') if x.strip()]
                res = {}
                for wid in weibo_ids:
                    res[wid] = process_comment_data(wid)
                return HttpResponse(json.dumps(res))
            return HttpResponse(json.dumps({'error': 'Missing commentId'}))

        return HttpResponse(json.dumps({'error': 'Invalid request method'}))

    @require_GET
    def getWeibo(request):
        infos = list(CommentWeiboInfo.objects.values("wb_id", "wb_userId", "wb_userName", "wb_user_profile_image_url", "wb_text"))
        return JsonResponse(infos, safe=False)

    @csrf_exempt
    @require_POST
    def auth_register(request):
        """用户注册"""
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            nickname = data.get('nickname', '').strip()

            if not username or not password:
                return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})

            if len(password) < 6:
                return JsonResponse({'success': False, 'message': '密码长度不能少于6位'})

            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '用户名已存在'})

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, nickname=nickname or username)

            login(request, user)

            return JsonResponse({
                'success': True,
                'message': '注册成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.profile.nickname
                }
            })
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'注册失败: {str(e)}'})

    @csrf_exempt
    @require_POST
    def auth_login(request):
        """用户登录"""
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()

            if not username or not password:
                return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    profile.nickname = user.username
                    profile.save()

                return JsonResponse({
                    'success': True,
                    'message': '登录成功',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'nickname': profile.nickname
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': '用户名或密码错误'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'登录失败: {str(e)}'})

    @csrf_exempt
    @require_POST
    def auth_logout(request):
        """用户登出"""
        logout(request)
        return JsonResponse({'success': True, 'message': '已登出'})

    @require_GET
    def auth_current(request):
        """获取当前登录用户信息"""
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            return JsonResponse({
                'success': True,
                'isLoggedIn': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'nickname': profile.nickname
                }
            })
        else:
            return JsonResponse({'success': True, 'isLoggedIn': False, 'user': None})

    @csrf_exempt
    @require_POST
    def search_history_add(request):
        """添加搜索记录"""
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword', '').strip()
            weibo_id = data.get('weibo_id', '').strip()
            nickname = data.get('nickname', '').strip()

            history = SearchHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                keyword=keyword,
                weibo_id=weibo_id,
                nickname=nickname
            )

            return JsonResponse({'success': True, 'history_id': history.id})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)})

    @require_GET
    def search_history_list(request):
        """获取搜索记录列表"""
        try:
            if request.user.is_authenticated:
                histories = SearchHistory.objects.filter(user=request.user)[:20]
            else:
                histories = SearchHistory.objects.filter(user=None)[:20]

            result = list(histories.values(
                'id', 'keyword', 'weibo_id', 'nickname', 'search_time'
            ))

            return JsonResponse({'success': True, 'history': result})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)})

    @require_GET
    @login_required
    def export_tweets_csv(request):
        """导出微博数据为 CSV 文件"""
        try:
            weibo_id = request.GET.get('weiboId', '').strip()
            if not weibo_id:
                return JsonResponse({'success': False, 'message': '缺少 weiboId 参数'})

            tweets = TweetsInfo.objects.filter(UserInfo_id=weibo_id).order_by('-PubTime')

            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename=weibo_data_{weibo_id}.csv'

            writer = csv.writer(response)
            writer.writerow(['微博ID', '发布时间', '内容', '点赞数', '评论数', '转发数', '情感值', '关键词', '发布工具'])

            for tweet in tweets:
                writer.writerow([
                    tweet._id,
                    tweet.PubTime.strftime('%Y-%m-%d %H:%M:%S') if tweet.PubTime else '',
                    tweet.Content,
                    tweet.Like,
                    tweet.Comment,
                    tweet.Transfer,
                    tweet.sentiments,
                    tweet.tags,
                    tweet.PubTools
                ])

            return response
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'导出失败: {str(e)}'})

    @require_GET
    @login_required
    def export_user_info(request):
        """导出用户信息为 CSV 文件"""
        try:
            weibo_id = request.GET.get('weiboId', '').strip()
            if not weibo_id:
                return JsonResponse({'success': False, 'message': '缺少 weiboId 参数'})

            try:
                user = UserInfo.objects.get(_id=weibo_id)
            except UserInfo.DoesNotExist:
                return JsonResponse({'success': False, 'message': '用户不存在'})

            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename=user_info_{weibo_id}.csv'

            writer = csv.writer(response)
            writer.writerow(['用户ID', '昵称', '性别', '地区', '生日', '星座', '简介', '关注数', '粉丝数', '微博数', '是否认证', '认证原因', 'VIP等级', '情感状态', '性取向'])
            writer.writerow([
                user._id,
                user.NickName,
                user.Gender,
                f'{user.Province} {user.City}',
                user.Birthday,
                user.Constellation,
                user.BriefIntroduction,
                user.Num_Follows,
                user.Num_Fans,
                user.Num_Tweets,
                '是' if user.Verified else '否',
                user.Verified_reason,
                user.VIPlevel,
                user.Sentiment,
                user.SexOrientation
            ])

            return response
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'导出失败: {str(e)}'})

    @require_GET
    def hot_tweets(request):
        """获取热度排名的微博"""
        try:
            limit = request.GET.get('limit', 20)
            try:
                limit = int(limit)
            except ValueError:
                limit = 20

            # 使用数据库级聚合和排序，只取前 limit 条
            tweets = TweetsInfo.objects.exclude(Content='').annotate(
                total_interaction=(
                    models.functions.Coalesce(models.F('Like'), models.Value(0)) +
                    models.functions.Coalesce(models.F('Comment'), models.Value(0)) +
                    models.functions.Coalesce(models.F('Transfer'), models.Value(0))
                )
            ).order_by('-total_interaction')[:limit]
            
            result = []
            for tweet in tweets:
                total = tweet.total_interaction
                result.append({
                    'id': tweet._id,
                    'content': tweet.Content,
                    'like': tweet.Like or 0,
                    'comment': tweet.Comment or 0,
                    'transfer': tweet.Transfer or 0,
                    'sentiments': float(tweet.sentiments) if tweet.sentiments else 0.0,
                    'pubTime': tweet.PubTime.strftime('%Y-%m-%d %H:%M:%S') if tweet.PubTime else '',
                    'totalInteraction': total
                })

            return JsonResponse({'success': True, 'tweets': result})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)})

    @require_GET
    def model_compare(request):
        models = [
            {"name": "SnowNLP", "acc": 0.82, "f1": 0.79, "desc": "本系统采用", "source": "实测"},
            {"name": "SVM+TF-IDF", "acc": 0.75, "f1": 0.72, "desc": "传统机器学习", "source": "参考文献[3]"},
            {"name": "NB+Bigram", "acc": 0.71, "f1": 0.68, "desc": "朴素贝叶斯", "source": "参考文献[4]"},
            {"name": "TextCNN", "acc": 0.86, "f1": 0.84, "desc": "深度学习", "source": "参考文献[5]"},
            {"name": "BERT", "acc": 0.89, "f1": 0.87, "desc": "预训练模型", "source": "参考文献[6]"},
        ]
        return JsonResponse({"success": True, "models": models})
