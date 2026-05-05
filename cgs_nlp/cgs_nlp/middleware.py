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
        # 如果是 API 请求且收到 302 重定向到登录页，转换为 403
        if response.status_code == 302 and '/admin/login/' in response.get('Location', ''):
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'success': False,
                    'message': '请先登录'
                }, status=403)
        return response
