"""
@author: Caesar
@file: comment.py
@time: 2022/7/24
"""
from rest_framework import serializers
from apis import models


class CreateCommentSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.Comment
        fields = ['news', "reply", "content", 'depth', "create_datetime"]
        read_only_fields = ['depth', ]
        extra_kwargs = {'news': {'write_only': True}}


class ListCommentSerializer(serializers.ModelSerializer):
    """
    func: serializer multiple-class comments, and children field is responsible to contain children comment of current one-class comment.
    """
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # SerializerMethodField() is similar as foreign key;
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        # nested construction is first.
        fields = ['children', "reply", "content", 'create_datetime']

    def get_children(self, obj):
        """
        func: first loop is responsible to get all child comment of one-class comment
              second loop is responsible to assign multiple-class comment in classes
        param: obj originate from view function: queryset
        """
        # id = comment_id, fetch children comments of one-class comments
        descendant_queryset = models.Comment.objects.filter(root=obj).order_by('id')

        descendant_dict = {}

        for descendant in descendant_queryset:
            """
            {
                 "2": {
                      "children": [],
                      "reply": 1,
                      "content": "请不要发布无关评论",
                      "depth": 1,
                      "create_datetime": "2022-07-24 22:15:48"
                 },
                 "3": {
                      "children": [],
                      "reply": 2,
                      "content": "评论区都能吵起来？我附议",
                      "depth": 2,
                      "create_datetime": "2022-07-24 22:16:42"
                 }
            }
            """
            ser = CreateCommentSerializer(instance=descendant, many=False)
            row = {'children': []}
            row.update(ser.data)
            descendant_dict[descendant.id] = row

        children_list = []
        for cid, item in descendant_dict.items():
            """
            children": [
                {
                    "children": [
                        {
                            "children": [],
                            "reply": 2,
                            "content": "评论区都能吵起来？我附议",
                            "depth": 2,
                            "create_datetime": "2022-07-24 22:16:42"
                        }
                    ],
                    "reply": 1,
                    "content": "请不要发布无关评论",
                    "depth": 1,
                    "create_datetime": "2022-07-24 22:15:48"
                }
            ],
            """
            depth = item['depth']
            if depth == 1:
                children_list.append(item)
                continue
            # sorted by comment_id
            comment_id = item['reply']
            # one dimension: comment_id; two dimension: children; replace comment_id by children comments;
            descendant_dict[comment_id]['children'].append(item)

        return children_list
