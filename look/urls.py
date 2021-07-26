from django.urls import path, re_path
from . import views  # url匹配成功则需要进入views视图给请求提供相应

urlpatterns = [
    path("index/<int:object>/", views.index, name='index'),
    path("index/look/", views.look, name='look'),
    path("test/", views.test, name='test'),
    re_path("^home/(?P<yy>[09]+)/$", views.test, name='home'),
    path("add_department/", views.add_department, name='add_department'),  # 向数据库添加学院信息，包括ID以及名称
    path("add_student/", views.add_student, name='add_student'),  # 向数据库添加学生信息，名字和ID
    # 关联数据表的使用，通过学生ID查询学院
    path("research_by_filter/", views.research_by_filter, name='research_by_filter'),  # 使用filter方法查询数据
    # 关联数据表的使用，通过学院查询学生ID
    path("research_by_filter2/", views.research_by_filter2, name='research_by_filter2'),  # 使用filter方法查询数据
    path("main_site/", views.main_site, name='main_site'),  # 使用filter方法查询数据
    path("id_request/", views.id_request, name='id_request'),  # 查询学院ID小于学生学号的数据对象：查询成功，使用F查询方法。
    path("add_age/", views.add_age, name='add_age'),  # 为每个学生的年龄增加一，使用F查询方法。
    path("alternative/", views.alternative, name='alternative'),  # 使用Q查询，张三或者王九，二者择其一。
    # 使用Q查询，实现两种不同字段的二选一查询。
    path("alternative_different_field/", views.alternative_different_field, name='alternative_different_field'),
    path('login_auth/', views.login_auth, name="login_auth"),  # 使用user表创建登录页面
    path('logout_auth/', views.logout_auth, name="login_auth"),  # 使用user表创建退出页面

]
