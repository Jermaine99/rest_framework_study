from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from api import models


class MyAuthentication(BaseAuthentication):
    """
        认证类必须继承BaseAuthentication
    """

    def authenticate(self, request):
        token = request._request.GET.get("token")
        if token is None:
            token = request._request.POST.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.NotAuthenticated("用户认证失败")
        return (token_obj.user, token_obj)

    def authenticate_header(self, val):
        pass
