# 注册功能中的创建类
from rest_framework import mixins
from rest_framework.response import Response
from apis.extension import returnCode


class DigCreateModelMixin(mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        """
        """
        # print(request.data, "接收前端信息，准备序列化")
        serializer = self.get_serializer(data=request.data)
        # print(serializer, "序列化部件")
        # serializer.is_valid(raise_exception=True)
        # 1. 异常处理：使用自定义的返回码
        if not serializer.is_valid():
            return Response({"code": returnCode.VALIDATE_ERROR, "detail": serializer.errors})
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # 2. 用户可以在执行创建函数中自定义返回值，该函数没有返回值时再返回自定义返回码
        res = self.perform_create(serializer)
        return res or Response({"code": returnCode.SUCCESS, "detail": serializer.data})
        # if not res:
        #     # 3. 返回数据的处理
        #     return Response({"code": returnCode.SUCCESS, "detail": serializer.data})
        # # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return res


class DigDestroyModelMixin(mixins.DestroyModelMixin):
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        res = self.perform_destroy(instance)
        return res or Response({"code": returnCode.SUCCESS})


class DigUpdateModelMixin(mixins.UpdateModelMixin):
    """
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({"code": returnCode.VALIDATE_ERROR, "detail": serializer.errors})
        res = self.perform_update(serializer)
        return res or Response({"code": returnCode.SUCCESS, "detail": serializer.data})


class DigListModelMixin(mixins.ListModelMixin):
    """
    queryset need to be introduced
    paginate: arrange page code.
    """
    def list(self, request, *args, **kwargs):
        #
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({"code": returnCode.SUCCESS, 'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": returnCode.SUCCESS, 'data': serializer.data})
