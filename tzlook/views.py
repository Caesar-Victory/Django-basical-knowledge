import os
from django.shortcuts import render, redirect, reverse
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
        fl.name = os.path.join(MEDIA_ROOT, fl.name)  # 文件名按照本身的文件名保存
        with open(fl.name, 'wb') as f:
            for c in fl.chunks():
                f.write(c)
            return HttpResponse('成功读取，已结束。')
    else:
        return HttpResponse('ERROR')


def set_cookie(request):
    '''
    设置cookies
    '''
    response = HttpResponse('设置cookie')
    response.set_cookie('name')  # 默认关闭浏览器则过期
    response.set_cookie('taka')  # 默认关闭浏览器则过期
    return response


def get_cookies(request):
    '''
    获取cookie
    '''
    cookie = request.COOKIES
    print(cookie)
    return HttpResponse("获取cookie")


def delete_ck(request):
    '''
    用什么方法创建就用什么方法删除
    '''
    rs = HttpResponse('删除cookie')
    rs.delete_cookie('name')
    return rs


def home1(request):
    username = request.session.get('username', '未登录')
    return render(request, 'user/home.html', context={'username':username})


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login2.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        # 使用session状态保持
        request.session['username'] = username
        request.session.set_expiry(None)
        # 重定向
        return redirect(reverse('home1'))


def logout(request):
    # 退出登录的逻辑
    # 1. 退出状态，在session
    request.session.flush()
    return redirect(reverse('home1'))
