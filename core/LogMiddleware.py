import json
import logging
import threading
from django.utils.deprecation import MiddlewareMixin

local = threading.local()

Logger = logging.getLogger('api')


class RequestLogFilter(logging.Filter):
    """
    日志过滤器
    """

    def filter(self, record):
        record.sip = getattr(local, 'sip', 'none')
        record.dip = getattr(local, 'dip', 'none')
        record.body = getattr(local, 'body', 'none')
        record.path = getattr(local, 'path', 'none')
        record.method = getattr(local, 'method', 'none')
        record.username = getattr(local, 'username', 'none')
        record.code = getattr(local, 'code', 'none')
        record.reason = getattr(local, 'reason', 'none')

        return True


class RequestLogMiddleware(MiddlewareMixin):
    """
    将request的信息记录在当前的请求线程上。
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()

        if request.method == 'GET':
            body.update(dict(request.GET))
        else:
            body.update(dict(request.POST))
        local.body = body
        local.path = request.path
        local.method = request.method
        local.username = request.user
        local.sip = request.META.get('REMOTE_ADDR', '')
        response = self.get_response(request)
        local.code = response.status_code
        local.reason = response.reason_phrase
        Logger.info('Nothing')

        return response
