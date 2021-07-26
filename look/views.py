from django.db.models import F, Q
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse  # 导入响应类
import datetime
from look.models import Student, Department
from book.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Permission, Group
# from look.forms import AddForm


# Create your views here.

def index(request, object):
    print(object, type(object))
    return HttpResponse('hello %s' % object)


def home(request, **kwargs):
    if kwargs.get('switch') == 'true':
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
        'name': name,
        'protagonist': protagonist,
        'books_name': '我是书的名字'
    }
    return render(request, 'indexxx.html', context)


def add_department(request):
    # de = Department(d_id=2, d_name='文学院2')
    # de.save()
    de = Department.objects.create(d_id=3, d_name='计算机学院')
    return HttpResponse('添加文学院2以及ID成功！')


def add_student(request):
    """
    添加学生信息
    """
    st = Student(s_id=1, s_name='张三', department_id=1)  # , department_id=1
    st.save()
    return HttpResponse('添加学生张三，id为1,成功！')


def research_by_filter(request):
    dat = Department.objects.filter(student__s_id=1)
    print(dat)
    print("在学院表中查询学号为1的学生：{}".format(dat))
    return HttpResponse("得偿所愿")


def research_by_filter2(request):
    dat = Student.objects.filter(department__d_id=3)
    print(dat)
    print("在学生表中查询学号为1的学生：{}".format(dat))
    return HttpResponse("得偿所愿")


def main_site(request):
    return render(request, 'base/base1.html')


def id_request(request):
    outcome = Student.objects.filter(department_id__lt=F('s_id'))
    print(outcome)
    return HttpResponse("查询学院ID小于学生学号的数据对象：查询成功")


def add_age(request):
    consequence = User.objects.all().update(age=F('age') + 1)
    print(consequence)
    return HttpResponse("为每个学生的年龄增加一，使用F查询方法。")


def alternative(request):
    ob = User.objects.filter(Q(name='张三') | Q(name='王九'))
    print(ob)
    return HttpResponse("使用Q查询，张三或者王九，二者择其一")


def alternative_different_field(request):
    ob = User.objects.filter(Q(name='李四') & Q(age=17))
    print(ob)
    print(type(ob))
    return render(request, 'loads.html', context={'ob': ob})


# def add_form(request):
#     if request.method == 'POST':
#         form = AddForm(request.POST)
#         if form.is_valid():
#             a = form.cleand_data['a']
#             b = form.cleand_data['b']
#             return HttpResponse(str(int(a)) + str(int(b)))
#         else:
#             form = AddForm()
#     return render(request, 'user/add_form.html')


def login_auth(request):
    if request.method == 'GET':
        return render(request, 'user/login2.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        # 使用session状态保持
        # request.session['username'] = username
        # request.session.set_expiry(None)
        # 重定向
        login(request, username)
        return redirect(reverse('home1'))


def home1(request):
    username = request.session.get('username', '未登录')
    return render(request, 'user/home.html', context={'username':username})


def logout_auth(request):
    # 退出登录的逻辑
    # 1. 退出状态，在session
    # request.session.flush()
    logout(request)
    return redirect(reverse('home1'))