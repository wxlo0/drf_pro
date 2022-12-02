from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from core.LogMiddleware import Logger


def common_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        Logger.error('ERROR!!!!!\nERROR!!!!!\nERROR!!!!!\nAn error occurred in the %s\n'
                     'The error that happens is %s' % (context['view'].__class__.__name__, str(exc)))
        response = Response({'code': 500, 'detail': '未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response.data['code'] = response.status_code
        if response.data.get('detail'):
            response.data['msg'] = response.data.pop('detail')
    return response


class RequestException(APIException):
    """
    serializers自定义错误响应
    """
    def __init__(self, error, code=400):
        self.detail = error
        self.status_code = code


