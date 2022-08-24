from apis.extension.mixins import DigCreateModelMixin, DigListModelMixin
from rest_framework.viewsets import GenericViewSet
from apis.extension.filter import SelfFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from apis import models
from apis.serializers.news import NewsSerializer
from django_filters import FilterSet, filters
from apis.extension.throttle import NewsCreateRateThrottle
from apis.extension.auth import UserAnonTokenAuthentication
from apis.serializers.news import IndexSerializer


class NewsFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = models.News
        fields = ["latest_id", ]


class NewsView(DigCreateModelMixin, DigListModelMixin, GenericViewSet):
    """
    filter topic without considering status of topic whether is published or not
    """
    # assure queryset belongs to currently logged-in user
    throttle_scope = 'upload'
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = NewsFilterSet
    # not be deleted;
    queryset = models.News.objects.filter(deleted=False).order_by("-id")
    serializer_class = NewsSerializer

    global_throttle = [NewsCreateRateThrottle(), ]

    def perform_create(self, serializer):
        """
        for topic, sell oneself
            two ways: add comment amount in apis.topic.
                      add record in apis. recommend
        """
        serializer.save(user=self.request.user)
        for throttle in self.get_throttles():
            throttle.done()

    def get_throttles(self):
        """
        throttle for post data, get data is excluded;
        """
        if self.request.method == "POST":
            return self.global_throttle
        return []


class IndexFilterSet(FilterSet):
    """
    func: provide filter service for fields: latest_id, zone

    post data: if not post zone, default: fetch all news.
    post format: ?zone=3 && latest_id = 4
    """

    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = models.News
        fields = ["latest_id", "zone"]


class IndexView(DigListModelMixin, GenericViewSet):
    """
    func: provide information of four zones: (1, "42区"), (2, "段子"), (3, "图片"), (4, "挨踢1024"), (5, "你问我答")

        four subclass: filter, authentication, queryset, serializer
            authentication: exist global configuration, we must override this class. otherwise,
                            front page is visible for every one.
            queryset: For fetching more data, we give up to setting filter condition: status=2, which mean to
                      information posted by user is censored.
                      Meanwhile, sort condition is variable. the functionality of sorting by id or create_time is equal,
                      id of topic is created by time order.

    """
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IndexFilterSet
    authentication_classes = [UserAnonTokenAuthentication, ]
    # filter condition: id's effect is equal to create_time because id assigned by create_time
    queryset = models.News.objects.filter(deleted=False).order_by("-id")
    # censored content
    # queryset = models.News.objects.filter(deleted=False, status=2).order_by("-id")
    serializer_class = IndexSerializer
