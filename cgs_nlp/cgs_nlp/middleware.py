from django.http import JsonResponse


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response


class LoginRequiredJSONMiddleware:
    """将 @login_required 的 302 重定向转换为 403 JSON 响应（针对 API 请求）"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 302:
            location = response.get('Location', '')
            if '/login/' in location:
                if request.path.startswith('/api/') or request.path.startswith('/cancelscrapyd'):
                    return JsonResponse({
                        'success': False,
                        'message': '请先登录'
                    }, status=403)
        return response
