from django.contrib import admin
from django.urls import include, path, re_path
from . import views  # url匹配成功则需要进入views视图给请求提供相应
from tzlook import urls

urlpatterns = [
    path("index/<int:object>/", views.index, name='index'),
    path("index/look/", views.look, name='look'),
    path("test/", views.test, name='test'),
    re_path("^home/(?P<yy>[09]+)/$", views.test, name='home'),
    path('', include('tzlook.urls')),
    #re_path("look/", include('look.urls'), {'switch':'true'}),
]
