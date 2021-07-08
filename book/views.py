from django.shortcuts import render
from .models import User, BookInfo
from django.http import HttpResponse


# Create your views here.
def article_new(request):
    name = 'Alex'
    context = {
        'name': 'python',
    }
    return render(request, 'look.html', context)


def test_01(request):
    ls = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    context = {
        'ls': ls,
    }
    return render(request, 'test.html', context)


# def test_01(request, xx):
#     # return render(request, 'test.html')
#     return HttpResponse(xx)


def heritage(request):
    return render(request, 'indexxx.html')


def common(request):
    somevariable = 'YKK   seasame'
    return render(request, 'loads.html', context={
        'somevariable': somevariable,
    })


def show_tag(request):
    return render(request, 'show_tag.html')


def index_01(request):
    '''
    all()查询出来的是一个对象
    get()查询出来的是某个属性
    '''
    user = User.objects.all()
    return render(request, 'database-book.html', context={'user': user})


def add_user(request):
    '''
    测试数据库的增加操作
    '''
    user = User(name='花无缺', age=17, gender=False)  # 字段值的写入一定要与其属性匹配
    user.save()
    return HttpResponse('添加成功')


def search_user(request):
    '''
    查询数据
    '''
    search = User.objects.all()
    # print(search)
    # return HttpResponse('查询成功，结果为：{}'.format(search))
    return HttpResponse('查询成功!')
    # return render(request, 'database-book.html', context=search)


def delete_user(request):
    '''
    通过指定ID，删除数据
    '''
    User.objects.get(id=2).delete()
    return HttpResponse('删除成功')


def update_user(request):
    '''
    修改成功
    '''
    user = User.objects.get(name='画龙老师')
    user.name = '徐媛老师'
    user.save()
    return HttpResponse('更新成功')

def modified_user(request):
    ''''
    修改数据，使用User.objects.filter().update()
    '''
    User.objects.filter(name='斗鱼').update(name='熊猫TV')
    return HttpResponse('第二种方法修改数据成功')


def ModifiedWholeFiled(request):
    ''''
    修改数据整个字段
    '''
    User.objects.update(age=18)
    return HttpResponse('修改全部字段成功')


def add_book(request):
    '''
    添加书籍名称
    '''
    book = BookInfo(name='Python Django开发实战', book_id=1)
    book.save()
    return HttpResponse("书籍：Python Django开发实战， 已经添加成功")


def search_book(request):
    user = User.objects.get(id=3)
    user.bookinfo_set.all()
    print(user)
    return HttpResponse("按照书籍id查询数据成功，书名为：{}".format(user))