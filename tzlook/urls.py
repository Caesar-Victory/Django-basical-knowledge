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
    path('main_pag', views.index_4),
    path('', include('book.urls')),
]
