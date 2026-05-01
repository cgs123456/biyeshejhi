from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.conf import settings
from SpiderAPI.models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo
from collections import Counter
from SnowNLPAPI.snownlp import SnowNLP
from os import path
import requests
import json
import re
import jieba
import os
import logging

# 配置日志
logger = logging.getLogger('ScrapydAPI')


class ScrapydWeibo:
    # Scrapyd 服务配置 - 从 settings 读取
    SCRAPYD_URL = getattr(settings, 'SCRAPYD_URL', 'http://localhost:6800')
    MAX_RETRIES = getattr(settings, 'SCRAPYD_MAX_RETRIES', 3)
    
    @csrf_exempt
    def ScrapydAPI(request):
        if request.method == "POST":
            # POST 方法需要登录
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'message': '请先登录'
                }, status=401)
                
            # 安全解析 weiboIds 参数
            weibo_ids_str = request.POST.get("weiboIds", "")
            ids = [x.strip() for x in weibo_ids_str.split(',') if x.strip()]
            cookies = request.POST.get("cookies", "")
            
            target_list_to_insert = list()
            duplicate_count = 0
            for id in ids:
                target = Target()
                target.uid = id
                target.cookie = cookies
                try:
                    Target.objects.get(uid=target.uid)
                    duplicate_count += 1
                except Target.DoesNotExist:
                    target_list_to_insert.append(target)
            
            if target_list_to_insert:
                Target.objects.bulk_create(target_list_to_insert)
                logger.info(f"成功添加用户数: {len(target_list_to_insert)}")
            if duplicate_count:
                logger.info(f"跳过重复用户数: {duplicate_count}")
            
            # Scrapyd 调度 - 添加重试逻辑
            url = ScrapydWeibo.SCRAPYD_URL + '/schedule.json'
            data = {'project': 'bot', 'spider': 'weibo_spider'}
            
            # 简单的重试逻辑
            schedule_response = None
            for retry in range(ScrapydWeibo.MAX_RETRIES):
                try:
                    schedule_response = requests.post(url=url, data=data, timeout=10)
                    schedule_response.raise_for_status()
                    logger.info("Scrapyd 调度成功")
                    break  # 成功，退出重试循环
                except requests.RequestException as e:
                    logger.warning(f"Scrapyd 连接失败 (尝试 {retry+1}/{ScrapydWeibo.MAX_RETRIES}): {str(e)}")
                    if retry == ScrapydWeibo.MAX_RETRIES - 1:
                        logger.error(f"Scrapyd 服务不可用: {str(e)}")
                        return JsonResponse({
                            'success': False,
                            'message': 'Scrapyd 服务不可用',
                            'error': str(e)
                        }, status=503)
            
            # 返回统一 JSON 格式
            if schedule_response:
                try:
                    scrapyd_result = schedule_response.json()
                    return JsonResponse({
                        'success': True,
                        'message': '任务提交成功',
                        'result': scrapyd_result
                    })
                except Exception as e:
                    return JsonResponse({
                        'success': True,
                        'message': '任务已提交，解析返回失败',
                        'raw_response': schedule_response.text
                    })
            return JsonResponse({
                'success': False,
                'message': '未知错误'
            }, status=500)
        
        if request.method == "GET":
            # Scrapyd 状态检查 - 不需要登录，公开访问
            requrl = ScrapydWeibo.SCRAPYD_URL + "/daemonstatus.json"
            try:
                result = requests.get(requrl, timeout=5)
                try:
                    status_data = result.json()
                    return JsonResponse({
                        'success': True,
                        'data': status_data
                    })
                except:
                    return JsonResponse({
                        'success': True,
                        'raw_response': result.text
                    })
            except requests.RequestException as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Scrapyd 服务不可用',
                    'error': str(e)
                }, status=503)

    @login_required
    @require_POST
    @csrf_exempt
    def CancelScrapyd(request):
        if request.method == "POST":
            jobId = request.POST.get("job", "")
            if not jobId:
                return JsonResponse({
                    'success': False,
                    'message': '缺少 jobId 参数'
                }, status=400)
                
            url = ScrapydWeibo.SCRAPYD_URL + "/cancel.json"
            data = {'project': 'bot', 'job': jobId}
            
            try:
                result = requests.post(url=url, data=data, timeout=10)
                try:
                    result_data = result.json()
                    return JsonResponse({
                        'success': True,
                        'data': result_data
                    })
                except:
                    return JsonResponse({
                        'success': True,
                        'raw_response': result.text
                    })
            except requests.RequestException as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Scrapyd 服务不可用',
                    'error': str(e)
                }, status=503)

    @require_GET
    def getLasted(request):
        infos = UserInfo.objects.values('_id', 'Image', 'NickName').order_by('-_id')
        user = json.dumps(list(infos), cls=DjangoJSONEncoder)
        targets = Target.objects.values("uid")
        target = json.dumps(list(targets), cls=DjangoJSONEncoder)
        result = {
            'user': user,
            'target': target,
            'count': json.dumps([])
        }
        print(result)
        return JsonResponse(result, safe=False)

    def getGroupInfo(request):
        result = []
        if request.method == "POST":
            ids = request.POST.get("weiboIds").split(',')
            for id in ids:
                alluser = UserInfo.objects.filter(_id=id)
                result.append({
                    'user': serializers.serialize('json', alluser)
                })
            return JsonResponse(result, safe=False)

        if request.method == "GET":
            # 安全地解析和校验 weiboIds 参数
            weibo_ids_str = request.GET.get("weiboIds", "")
            ids = [x.strip() for x in weibo_ids_str.split(',') if x.strip().isdigit()]
            
            TweetsInfo.objects.filter(Content='').delete()

            stopwords_path = path.join(path.dirname(__file__), 'stopword.txt')
            mingan_path = path.join(path.dirname(__file__), 'mingan.txt')

            stopwords = set()
            if path.exists(stopwords_path):
                with open(stopwords_path, 'r', encoding='utf-8') as f:
                    stopwords = {line.strip() for line in f.readlines()}

            minganwords = set()
            if path.exists(mingan_path):
                with open(mingan_path, 'r', encoding='utf-8') as f:
                    minganwords = {line.strip() for line in f.readlines()}

            sentimentslist = []
            # 分批处理避免 OOM，不要一次性把所有内容拼进一个字符串
            all_content_parts = []
            for id in ids:
                infos = TweetsInfo.objects.filter(UserInfo_id=id).values('Content')
                for info in infos:
                    if info['Content']:
                        all_content_parts.append(info['Content'])
                        m = re.sub(r"[A-Za-z0-9\：\·\—\，\。\“ \” \? \@]", "", info['Content'])
                        if m:
                            s = SnowNLP(m)
                            sentimentslist.append(s.sentiments)
            # 只在需要时合并内容
            content = "".join(all_content_parts)

            c0 = Counter()
            for word0 in sentimentslist:
                c0[word0] += 1
            li0 = list(c0.items())
            li0.sort(key=lambda x: x[0])

            content = re.sub(r"[A-Za-z0-9\：\·\—\，\。\“ \”]", "", content)
            wordlist_after_jieba = jieba.cut(content, cut_all=False)
            wl_space_split = " ".join(wordlist_after_jieba)

            c = Counter()
            outstr_list = []
            for word in wl_space_split.split():
                if word and word not in stopwords and word not in ('\t', '\n', ' ', ''):
                    outstr_list.append(word)

            for word in outstr_list:
                c[word] += 1

            cipin = []
            li = list(c.items())
            li.sort(key=lambda x: x[1], reverse=True)
            mingancount = 0
            for (k, v) in li:
                if k in minganwords:
                    mingancount += 1
                cipin.append({"word": k, "count": v})

            # ================== 舆情预警逻辑 ==================
            total = len(sentimentslist)
            count0 = 0
            negative_ratio = 0
            warning = False
            warning_level = "normal"
            
            # 统计负面情绪数量（假设 <0.5 为负面）
            for (sentiment, count) in li0:
                if sentiment < 0.5:
                    count0 += count
            
            if total > 0:
                negative_ratio = count0 / total
            
            # 预警判定
            if negative_ratio >= 0.5:
                warning = True
                warning_level = "danger"  # 红色预警 - 高危
            elif negative_ratio >= 0.3:
                warning = True
                warning_level = "warning"  # 黄色预警 - 中危
            
            res = {
                "mingan": mingancount / len(li) if li else 0,
                "cipin": cipin[:200],
                "analy": li0,
                "warning": warning,
                "warning_level": warning_level,
                "negative_ratio": negative_ratio,
                "total_count": total
            }
            return JsonResponse(res, safe=False)
