"""tzlook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tzlook import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('detail/', views.mumu),
    # path('detail/<int:num>/', views.mumu),  # 写了两个近似路径，是为了对同一个response设置不同的返回结果，根据用户的输入决定返回对象
    path('main_pag/', views.index_4),
    path('', include('book.urls')),
    path('', include('look.urls')),
    path('get_test/', views.get_test),  # 测试Get方法,服务器获取浏览器输入的值
    path('req_test/', views.req_test),  # 测试Get方法，渲染整个HTML5
    path('post_test/', views.post_test),  # 测试Get方法，同时处理两种请求
    path('clas_add/', views.BlogAdd.as_view(), name="clas_add"),  # django.db.Views重构
    path('upload_test/', views.upload_test, name="upload_test"),  # 文件上传
    path('set_cookie/', views.set_cookie, name="set_cookie"),  # 设置cookies
    path('get_cookies/', views.get_cookies, name="get_cookies"),  # 获取cookies
    path('delete_ck/', views.delete_ck, name="delete_ck"),  # 删除cookies
    path('home1/', views.home1, name="home1"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
