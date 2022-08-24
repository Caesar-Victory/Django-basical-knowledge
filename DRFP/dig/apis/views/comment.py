"""
@author: Caesar
@file: comment.py
@time: 2022/7/24
"""
import datetime
from rest_framework.viewsets import GenericViewSet
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from apis import models
from apis.serializers.comment import CreateCommentSerializer, ListCommentSerializer
from apis.extension.filter import SelfFilterBackend
from apis.extension.mixins import DigCreateModelMixin, DigListModelMixin
from apis.extension.auth import TokenAuthentication


class CommentFilterSet(FilterSet):
    news = filters.NumberFilter(field_name='news', required=True)
    latest_id = filters.DateTimeFilter(field_name='descendant_update_datetime', lookup_expr='lte')

    class Meta:
        model = models.Comment
        fields = ["latest_id", 'news']


class CommentView(DigListModelMixin, DigCreateModelMixin, GenericViewSet):
    """
    func: add comment and display comment.
    component: filter, authentication, queryset[lazy loading], serializer
    design: bypass: GET: no authentication; POST:TokenAuthentication.
    assignment: bypass--->get_serializer_class; get_authenticators.
                creation: perform_create
    test: url & parameters: POST method; p---> news: id, content: str, replay: id;
                            GET method: news
    """
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]

    filterset_class = CommentFilterSet

    # TokenAuthentication,
    authentication_classes = [TokenAuthentication, ]

    # display comment by time order. descendant_update_datetime: latest update
    # this tragedy influence one-class comment.
    queryset = models.Comment.objects.filter(depth=0).order_by("-descendant_update_datetime")

    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        """
        objects: location: root comment and one-class comment
                 component: user/user_id; create_time; content; news_id / comment_id
        """
        # fetch relay_id which is to locate comment_id
        reply = serializer.validated_data.get('reply')
        if not reply:
            # This sentence is equal to create new comment, Meanwhile, it will be considered as root comment.
            instance = serializer.save(user=self.request.user)
        else:
            if not reply.root:
                root = reply
            else:
                root = reply.root
            # elements: user_id, depth, and root
            instance = serializer.save(user=self.request.user, depth=reply.depth + 1, root=root)

            # modify latest updating of root as current time;
            root.descendant_update_datetime = datetime.datetime.now()
            root.save()
        # retrieve news table.
        instance.news.comment_count += 1
        instance.news.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListCommentSerializer
        return CreateCommentSerializer

    def get_authenticators(self):
        if self.request.method == "POST":
            return super().get_authenticators()
        return []
