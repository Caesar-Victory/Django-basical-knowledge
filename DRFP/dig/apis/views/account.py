# 注册功能的实现
from rest_framework.viewsets import GenericViewSet
from apis.extension.mixins import DigCreateModelMixin
from apis.serializers.account import RegisterSerializer
# 登录功能的实现
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import JsonResponse
from apis.extension import returnCode
from django.db.models import Q
from apis import models
import uuid, datetime
from apis.serializers.account import AuthSerializer


class RegisterView(DigCreateModelMixin, GenericViewSet):
    """"
    用户注册
        1. 仅需要提供 POST方法，因此使用自定义类
        2. 收到请求后执行 DigCreateModelMixin 的 create方法
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        # 保存时不需要重复记录密码
        print(serializer.validated_data, "序列化结束，执行用户创建")
        serializer.validated_data.pop("confirm_password")
        # super().perform_create(serializer)
        serializer.save()


class AuthView(APIView):
    """
    用户登录
            1. 获取用户请求 & 校验
            2. 数据库校验用户名和密码的合法性
    注意：   cookie有效期的设定需要配置正确的时间参照点，请在 settings中完成时区，数据库时间两个国际化功能
    """
    throttle_scope = 'uploads'
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        # print(serializer)
        if not serializer.is_valid():
            # serializer.error 内部会返回一个字典
            # 错误信息的存储格式： {"username": [错误信息，], "phone": [xxx, ]}
            # "error": "General error", 
            # return JsonResponse({"code": returnCode.VALIDATE_ERROR, "detail": serializer.errors})
            return Response({"code": returnCode.VALIDATE_ERROR, "detail": serializer.errors})

        username = serializer.validated_data.get("username")
        phone = serializer.validated_data.get("phone")
        # print(phone)
        password = serializer.validated_data.get("password")

        # https://docs.djangoproject.com/zh-hans/4.0/topics/db/queries/#complex-lookups-with-q-objects
        # Q 对象能通过 & 和 | 操作符连接起来。当操作符被用于两个 Q 对象之间时会生成一个新的 Q 对象。
        # print(username, password)
        # print(type(username), type(password))
        user_obj = models.UserInfo.objects.filter(Q(Q(username=username) | Q(phone=phone)),
                                                  password=password).first()

        if not user_obj:
            # return JsonResponse({"code": returnCode.VALIDATE_ERROR, "error": "用户名或者密码错误"})
            return Response({"code": returnCode.VALIDATE_ERROR, "error": "用户名或者密码错误"})

        # https://docs.python.org/zh-cn/3/library/uuid.html#module-uuid
        token = uuid.uuid5(uuid.NAMESPACE_DNS, 'www.luffy.com')
        # token = uuid.uuid4()
        # print(type(token))
        user_obj.token = token
        # user_obj.token = pickle.dumps(token)
        user_obj.token_expiry_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
        # k = user_obj.save()
        # print(k)
        # 该行主要测试代码的数据类型是否正确
        # <class 'str'> <class 'NoneType'> <class 'str'> <class 'str'>
        # print(type(username), type(phone), type(password), type(token))
        # 以下代码可以定位错误代码的行数
        # print(4)
        user_obj.save()
        # print(5)
        # return JsonResponse({"code": returnCode.SUCCESS, "data": {"token": token, "name": user_obj}})
        # return Response({"code": returnCode.SUCCESS, "data": {"token": token, "name": user_obj}})
        # 出现 model实例对象不可序列化的根源：user_obj.username 写为 user_obj
        return Response({"code": returnCode.SUCCESS, "data": {"token": token, "name": user_obj.username}})
