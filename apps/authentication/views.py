from rest_framework.response import Response
from rest_framework import generics, permissions, status


class Test(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        return Response({"code": 1})
