from django.contrib import admin
from django.urls import include, path, re_path
from . import views  # url匹配成功则需要进入views视图给请求提供相应

urlpatterns = [
    path("index/<int:object>/", views.index, name='index'),
    path("index/look/", views.look, name='look'),
    path("test/", views.test, name='test'),
    re_path("^home/(?P<yy>[09]+)/$", views.test, name='home'),
    path("add_department/", views.add_department, name='add_department'),  # 向数据库添加学院信息，包括ID以及名称
    path("add_student/", views.add_student, name='add_student'),  # 向数据库添加学生信息，名字和ID
]
