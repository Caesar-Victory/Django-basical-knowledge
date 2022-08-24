from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apis import models


class RegisterSerializer(serializers.ModelSerializer):
    """
    保存用户名密码时不需要记录确认密码
    """
    confirm_password = serializers.CharField(label="确认密码", write_only=True)
    password = serializers.CharField(label="密码", min_length=8, write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ['username', "phone", "password", "confirm_password"]

    def validate_username(self, value):
        exists = models.UserInfo.objects.filter(username=value, deleted=False).exists()
        if exists:
            raise ValidationError("用户名已占用")
        else:
            return value
        # print(value, "打印用户名")

    def validate_password(self, value):
        exists = models.UserInfo.objects.filter(phone=value, deleted=False).exists()
        if exists:
            raise ValidationError("手机号码已注册")
        else:
            return value
        # print(value, "打印密码")

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")
        print(password, "先打印从前端接收到的密码")
        print(value, "再打印从前端接收到的密码")
        if password == value:
            return value
        else:
            print(value, "打印确认密码")
            raise ValidationError("两次密码不一致")


class AuthSerializer(serializers.Serializer):

    """
    功能：分别序列化三个对象; 读写，必填为父类Field字段；子类CharField限定长度
    required=False, 可以不填写
    """
    username = serializers.CharField(label="用户名", write_only=True, required=False)
    # , min_length=11, max_length=11
    phone = serializers.CharField(label="手机号", write_only=True, required=False)
    password = serializers.CharField(label="密码", write_only=True, min_length=8)

    # class Meta:
    #     model = models.UserInfo
    #     fields = ['username', "phone", "password"]

    def validate_username(self, value):
        """
        逻辑：手机号可以作为用户名，因此二者只能择其一，前端提交两者则错误
        @param value:
        @return:
        """
        username = self.initial_data.get("username")
        phone = self.initial_data.get("phone")
        print(phone, username)

        if not username and not phone:
            raise ValidationError("用户名或者手机号为空")

        if username and phone:
            raise ValidationError("用户名或者手机号任选其一")
        # 测试序列化之后的数据格式
        # print(value)
        return value