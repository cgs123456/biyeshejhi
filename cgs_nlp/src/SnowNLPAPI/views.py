from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .snownlp import SnowNLP
from .snownlp import sentiment
import re


class SnowNLPWeibo:
    @require_GET
    def SnowNLPAPI(request):
        text = request.GET.get("snownlp", "")

        if not text or not text.strip():
            return JsonResponse({
                'sentiments': 0.5,
                'keywords': [],
                'tf': [],
                'words': [],
                'sentences': [],
                'tf2': [],
                'idf': [],
            })

        try:
            s = SnowNLP(text)
        except Exception:
            return JsonResponse({
                'sentiments': 0.5,
                'keywords': [],
                'tf': [],
                'words': [],
                'sentences': [],
                'tf2': [],
                'idf': [],
            })

        result = {}
        myset = set()
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z]")
        clean_text = cop.sub('', text)
        for ch in clean_text:
            if ch in myset:
                pass
            else:
                myset.add(ch)
        for ch in myset:
            result[ch] = clean_text.count(ch)
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)

        try:
            keywords = s.keywords(3)
        except Exception:
            keywords = []

        try:
            words = s.words
        except Exception:
            words = []

        try:
            sentences = s.sentences
        except Exception:
            sentences = []

        try:
            tf2 = s.tf
        except Exception:
            tf2 = []

        try:
            idf = s.idf
        except Exception:
            idf = []

        mm = {
            'sentiments': s.sentiments,
            'keywords': keywords,
            'tf': result,
            'words': words,
            'sentences': sentences,
            'tf2': tf2,
            'idf': idf,
        }
        return JsonResponse(mm)
