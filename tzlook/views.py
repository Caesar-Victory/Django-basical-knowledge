import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from tzlook.settings import MEDIA_ROOT

def hello():
    return 'django'


class Fruits:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def say(self):
        return 'Hello BlueCat'


ap = Fruits('apple', 'red')
ls = ['x', 'y', 'z']
dc = {'a': 1, 'b': 2}


def index_4(request):
    return render(request, 'tzlook/index.html',
                  context={'books_name': 'python',
                           'hello': 'hello',
                           'fruits_say': ap.say,
                           'fruits': ap,
                           'list': ls,
                           'dict': dc,
                           })


def get_test(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    print(a, b)
    return HttpResponse("测试GET方法")


def req_test(request):
    print(request.path)
    print(request.method)
    return render(request, "viewstest.html")


def post_test(request):
    if request.method == 'GET':
        return render(request, 'viewstest.html')
    elif request.method == 'POST':
        a = request.POST.get('a')
        b = request.POST.get('b')
        print(a, b)
        return HttpResponse('')
    else:
        return HttpResponse("这个不是一个可以处理的请求")


class BlogAdd(View):
    def get(self, request):
        return render(request, 'viewstest.html')

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog = BlogAdd(title, content)
        return HttpResponse('post请求。')


def upload_test(request):
    if request.method == 'GET':
        return render(request, 'ss.html')
    elif request.method == 'POST':
        fl = request.FILES.get('file')
        fl.name = os.path.join(MEDIA_ROOT, fl.name)
        with open(fl.name, 'wb') as f:
            for c in fl.chunks():
                f.write(c)
            return HttpResponse('成功读取，已结束。')
    else:
        return HttpResponse('ERROR')