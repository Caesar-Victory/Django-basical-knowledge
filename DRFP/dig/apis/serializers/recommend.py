"""
@author: Caesar
@file: recommend.py
@time: 2022/7/22
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apis import models
from apis.extension import returnCode


class RecommendSubNewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.News
        fields = ['id', 'title', 'url', "image_list"]

    def get_image_list(self, obj):
        if not obj.image:
            return []
        return obj.image.split(',')


class RecommendSerializer(serializers.ModelSerializer):
    """
    fuc:
    test: user only post news_id to server. user's name and id are checked by SelfFilterBackend
    """

    # https://www.django-rest-framework.org/api-guide/fields/#source
    news_info = RecommendSubNewsSerializer(read_only=True, source="news")

    class Meta:
        model = models.Recommend
        fields = ['id', "news", "news_info"]
        # when you need to add data, you must set field privilege as write_only,
        # the read_only field is considered as displaying news.
        extra_kwargs = {'news': {'write_only': True}}

    def validate_news(self, value):
        if value.deleted:
            raise ValidationError({"code": returnCode.NotExisting, "info": {"This news is not existed."}})
        return value
