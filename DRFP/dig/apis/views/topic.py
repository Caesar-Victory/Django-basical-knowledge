from rest_framework.viewsets import GenericViewSet
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from apis import models
# import self_made serializer to format data between front end and rear end
from apis.serializers.topic import TopicSerializer
# import self_made model to accomplish creation, delete, modification and search
from apis.extension.mixins import DigCreateModelMixin, DigDestroyModelMixin, DigUpdateModelMixin, DigListModelMixin

from apis.extension.filter import SelfFilterBackend


class TopicFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name="id", lookup_expr="lt")

    class Meta:
        model = models.Topic
        fields = ["latest_id", ]


class TopicView(DigCreateModelMixin, DigDestroyModelMixin, DigUpdateModelMixin, DigListModelMixin, GenericViewSet):
    """
    话题功能
    On GenericAPIView subclasses you may also set the pagination_class attribute to select LimitOffsetPagination on a per-view basis
    """
    filters_backends = [SelfFilterBackend, DjangoFilterBackend]
    # 暂时调用全局，特殊需求时再自定义
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    queryset = models.Topic.objects.filter(deleted=False).order_by('-id')

    #  be responsible to assure current user
    serializer_class = TopicSerializer

    # aim to filter proper amount of topic
    filterset_class = TopicFilterSet

    # pagination_class = None

    def perform_create(self, serializer):
        # 保存用户信息，便于删除通知
        # print(serializer)
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # logical delete
        instance.deleted = True
        instance.save()
