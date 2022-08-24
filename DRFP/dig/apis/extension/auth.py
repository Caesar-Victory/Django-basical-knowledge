import datetime
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apis.extension import returnCode
from apis import models


class TokenAuthentication(BaseAuthentication):
    """
    All authentication classes should extend BaseAuthentication.
    必须认证成功才能访问
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.query_params.get("token")

        if not token:
            raise AuthenticationFailed({"code": returnCode.AUTH_FAILED, "error": "认证失败"})
        user_object = models.UserInfo.objects.filter(token=token).first()

        if not user_object:
            raise AuthenticationFailed({"code": returnCode.AUTH_FAILED, "error": "认证失败"})

        if datetime.datetime.now() > user_object.token_expiry_date:
            raise AuthenticationFailed({"code": returnCode.AUTH_OVERDUE, "error": "认证过期"})

        return user_object, token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return "Powered by BiLiBiLi"


class UserAnonTokenAuthentication(BaseAuthentication):
    """
    匿名用户权限，request_user无值
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.query_params.get("token")

        if not token:
            return None

        user_object = models.UserInfo.objects.filter(token=token).first()

        if not user_object:
            return None

        if datetime.datetime.now() > user_object.token_expiry_date:
            return None

        return user_object, token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return "Powered by BiLiBiLi"
