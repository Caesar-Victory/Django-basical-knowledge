from rest_framework import serializers
from apis import models
from rest_framework.exceptions import ValidationError


class NewsSerializer(serializers.ModelSerializer):
    """
    1. Meta define specific model and fields.
    2. name must be consistent in serializer declaration and fields[in Meta]
    3. when creating news, we can use four fields: zone, title, topic, url, image
        1. only post pure text. provide four choices:
        2. post title and images;
        3. post url and title(or automatically generate);
    4. topic is optional, title is obligatory;
    fields:
        image_list: separate file name and source path with str.split()
        zone_title: flag is numeric but content is Chinese.
    what is the parameter:source?
    """
    image_list = serializers.SerializerMethodField(read_only=True)
    topic_title = serializers.CharField(source="topic.title", read_only=True)
    zone_title = serializers.CharField(source="get_zone_display", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = models.News
        fields = ["id", "title", "url",
                  "image", "topic", "zone",
                  "zone_title", "image_list", "topic_title",
                  "collect_count", "recommend_count", "comment_count",
                  "status"
                  ]

        read_only_fields = ["collect_count", "recommend_count", "comment_count"]

        extra_kwargs = {
            "image": {"write_only": True},
            "topic": {"write_only": True},
            "zone": {"write_only": True}
        }

    def get_image_list(self, obj):
        if not obj.image:
            return []
        return obj.image.split(",")

    def validated_topic(self, value):
        if not value:
            return value

        request = self.context['request']

        # topic 写为 news
        exists = models.Topic.objects.filter(deleted=False, id=value.id, user=request.user).exists()

        if not exists:
            raise ValidationError("The topic is not existed.")

        return value

    def validate_title(self, value):
        url = self.initial_data.get("url")
        image = self.initial_data.get("image")
        zone = self.initial_data.get("zone")

        if url and image:
            # raise 写为 return
            raise ValidationError("请求数据错误: query data is wrong.")

        if not url and not image:
            if zone == 3:
                raise ValidationError("所选分区错误:selected part is wrong.")

        return value

    def create(self, validated_data):
        """
        for topic, sell oneself
            two ways: add comment amount in apis.topic.
                      add record in apis. recommend
        """
        request = self.context['request']

        news_obj = models.News.objects.create(recommend_count=1, **validated_data)

        models.Recommend.objects.create(
            news=news_obj,
            user=request.user
        )

        return news_obj


class IndexSubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ['id', 'title', 'is_hot']


class IndexSubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['id', 'username', ]


class IndexSerializer(serializers.ModelSerializer):
    # Three fields will be lazy loading.
    image_list = serializers.SerializerMethodField()
    collect = serializers.SerializerMethodField()
    recommend = serializers.SerializerMethodField()

    # Three columns to display, user don't need to concern what can be modified.
    zone = serializers.CharField(source='get_zone_display')
    topic = IndexSubTopicSerializer(read_only=True)
    user = IndexSubUserSerializer(read_only=True)

    class Meta:
        model = models.News
        fields = ['id', "title", "url", 'image_list', 'topic', "zone", "user", 'collect',
                  'recommend', 'comment_count', ]

    def get_image_list(self, obj):
        # Fetch file name of picture
        if not obj.image:
            return []
        return obj.image.split(',')

    def get_collect(self, obj):
        request = self.context['request']
        # For user not logged in, display amount of collection, Anonymous user have not collection privilege.
        if not request.user:
            return {'count': obj.collect_count, 'has_collect': False}

        exists = models.Collect.objects.filter(user=request.user, news=obj).exists()
        return {'count': obj.collect_count, 'has_collect': exists}

    def get_recommend(self, obj):
        """
        Fetch amount of collection and comment, two function have similar construction.
        """
        request = self.context['request']
        if not request.user:
            return {'count': obj.recommend_count, 'has_recommend': False}
        exists = models.Recommend.objects.filter(user=request.user, news=obj).exists()
        return {'count': obj.recommend_count, 'has_recommend': exists}
