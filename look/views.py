from django.shortcuts import render
from django.http import HttpResponse  # 导入响应类
import datetime

# Create your views here.

def index(request, object):
    print(object, type(object))
    return HttpResponse('hello %s' % object)


def home(request, **kwargs):
    if kwargs.get('switch')=='true':
        print(datetime.datetime.now())
    return HttpResponse("这个是用re_path设置的")


def test(request, yy):
    print(yy, type(yy))
    return HttpResponse("这是一个使用了正则匹配的服务器资源访问路径,但更为复杂")


def mumu(request, num=1):
    if num == 1:
        return HttpResponse("这是一个默认页面")
    else:
        return HttpResponse("不想看到默认页面，于是你就来到了这里")


def look(request):
    name = 'T Y L O R'  # 在模板中使用删除空格的功能
    protagonist = 'Caesar'
    context = {
        'name' : name,
        'protagonist' : protagonist,
        'books_name': '我是书的名字'
    }
    return render(request, 'indexxx.html', context)