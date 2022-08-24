from rest_framework import routers
from apis.views import account, topic, news, collect, recommend, comment
from django.urls import path

router = routers.SimpleRouter()
router.register('register', account.RegisterView, 'register')

# 创建话题（认证）
router.register(r'topic', topic.TopicView)

# 我的资讯
router.register(r'news', news.NewsView)
#
# 资讯首页
router.register(r'index', news.IndexView)

# 收藏
router.register(r'collect', collect.CollectView)

# # 推荐
router.register(r'recommend', recommend.RecommendView)
#
# # 评论
router.register(r'comment', comment.CommentView)

urlpatterns = [
    # path('register/', account.RegisterView.as_view({"post": "create"})),
    path('auth/', account.AuthView.as_view()),
]

urlpatterns += router.urls
