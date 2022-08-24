# 项目介绍



1. 构建时间：20220713；1959
2. 项目进度：第三个功能—话题
3. 内容：
    1. 基于Django的 ```REST framework```框架
    2. 前后端分离项目，且组件分离；

4. 其他信息
    1. 官网：API—[Home - Django REST framework (django-rest-framework.org)](https://www.django-rest-framework.org/)
    2. one more thing: [Django REST Framework 3.13 -- Classy DRF (cdrf.co)](https://www.cdrf.co/)
    3. Conventional Commits[Git]: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)



# Schedule



2022.07.16

accomplished topic functionality which includes fetching topic, modification, delete and display limited information of topic.

2022.07.17

accomplished display of ```mynews```, which includes filter: assure current logged-in user to fetch own information and use serializer to serializer topic_title, zone_title, image_list and status;

2022.07.18

finished  a half of throttle functionality: achieve to throttle for creation of news. Main modification focus on parse_rate. At same time, complete temporary throttle according only preserve class: throttle_failure.

2022.07.19

when project keeps running, the cache must run, and cache_default is configured for news of pagination.

2020.07.20

It takes me one hour to solve problem that ```Field 'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x000001F34F32EA70>.```

we only need log in again which solve above problems. In the process of solving problem, I find that the sentence ```print()``` will be implemented by default, so by printing data judge what sentence is implemented is invalidated. 

2022.07.22



# Summary

1. 昨天在查看```rest_framework.serializers.ModelSerializer```源码时发现，有针对```UUID```类型的序列化类型，同理可得，model肯定也有，遂决定修改原来的```CharField``` 为```UUDIField```。迁移前后数据长度不一致，曾保持原有长度64，仍然迁移失败【外键关联无法删除当前数据表后重新迁移】后，使用UUID的长度36并删除所有的数据重新迁移（同时删除```migrations```下的迁移记录），重新迁移一举成功；说明表单在项目构建时就应该充分考虑好外键关联，数据类型等因素，开发过程中尽量不要修改数据格式。
2. 遇到一个bug，提示某个字段的数据为空，一般而言问题出在序列化中，将读写权限弄错。但是报错复现需要重写代码，立即想到使用log存储报错信息，便于记录报错信息复盘；
3. 限流类中，会将被限流的数据首先导入缓存中，因此实现此功能必须保持Redis缓存的实时运行。同时收到报错：键不是数值，而是字符串，还有键过长的问题，均是由于没有配置两个函数：get_cache_key, throttle_failure. 具体地，前者负责指定存储时的主键【Redis存储是以键值对的方式】，后者负责拒绝创建；
4. 经过调试发现，写在view试图中某个特定的类，打印语句并不能诊断代码执行到那个位置，从而定位bug。代码的运行逻辑是一开始直接运行当页的打印语句，无需URL链接到访特定view下的类再打印；凡是涉及到数据库查询的位置，此功能的笔记无可避免的应当写出model中的字段定义，否则模糊的印象会导致此后层出不穷的bug.
5. 调试后发现， 序列化中的 Field字段和数据库中的字段一一对应，作为返回值，用于展示一组信息的，同时也是一种声明；
6. 收藏功能在展示收藏的新闻时，可以做分页也可以不做。不指定分页的类时，系统默认分页十条新闻一页。但据观察，网站实际不做分页，因此我们需要在评论的视图中直接将分页类指定为None,这样就重写了全局分页；

# Format

1. ```MindMap```

2. Git 

    ```JSON
    fix: prevent racing of requests
    
    Introduce a request id and a reference to latest request. Dismiss
    incoming responses other than from latest request.
    
    Remove timeouts which were used to mitigate the racing issue but are
    obsolete now.
    
    Reviewed-by: Z
    Refs: #123
    ```

    

3. ```docstring```

    ```JSON
    func:
    para:
    ```

4. Test

    ```JSON
    request method:
    parameters:
    ```

5. Main Function

    ```python
        """
        func: add comment and display comment.
        component: filter, authentication, queryset[lazy loading], serializer
        design: bypass: GET: no authentication; POST:TokenAuthentication.
        assignment: bypass--->get_serializer_class; get_authenticators.
                    creation: perform_create
        """
    ```

# Test

```JSON
1. 一般使用print()函数打印当前数据，遇到多次打印时，可以在前面加入文字描述；
2. 可以直接打印数据对象，也可以打印成员数据，或者是直接打印数据类型；
```

