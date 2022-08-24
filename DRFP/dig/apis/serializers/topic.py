from rest_framework import serializers
from apis import models


class TopicSerializer(serializers.ModelSerializer):
    """
    Meta define specific model and fields
    """
    class Meta:
        # 错误写为models
        model = models.Topic
        fields = ["id", "title", "is_hot"]
        # 查找一下其下内容是否有该限制字段：https://www.django-rest-framework.org/api-guide/fields/
        # read_only_fields = ["is_hot"]
        extra_kwargs = {"is_hot": {"read_only": True}}
