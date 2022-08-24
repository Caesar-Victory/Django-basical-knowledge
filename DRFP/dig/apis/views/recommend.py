"""
@author: Caesar
@file: recommend.py
@time: 2022/7/22
"""

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from apis import models
from apis.serializers.recommend import RecommendSerializer
from apis.extension.filter import SelfFilterBackend
from apis.extension.mixins import DigCreateModelMixin, DigListModelMixin
from apis.extension import returnCode
from apis.extension.page import RecommendPagination

class RecommendFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = models.Recommend
        fields = ["latest_id", ]


class RecommendView(DigCreateModelMixin, DigListModelMixin, GenericViewSet):
    """
    func: implement collection and recommendation if database has not their data, others deleted their data when quest is posted.

    """
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = RecommendFilterSet

    # RecommendPagination
    pagination_class = RecommendPagination

    # queryset is public, which can be obtained by DigCreateModelMixin & DigListModelMixin.
    queryset = models.Recommend.objects
    serializer_class = RecommendSerializer

    def perform_create(self, serializer):
        """
        """
        user = self.request.user
        print(type(serializer.validated_data))
        instance = models.Recommend.objects.filter(user=user, **serializer.validated_data).first()
        if not instance:
            instance = serializer.save(user=user)
            instance.news.recommend_count += 1
            instance.news.save()
            return Response({"code": returnCode.SUCCESS, 'data': {'active': True}})
        else:
            instance.delete()
            instance.news.recommend_count -= 1
            instance.news.save()
            return Response({"code": returnCode.SUCCESS, 'data': {'active': False}})
