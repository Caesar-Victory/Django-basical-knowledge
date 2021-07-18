

# 自定义过滤器
# 注册自定义过滤器
from datetime import datetime
from django import template
import locale


locale.setlocale(locale.LC_CTYPE, 'chinese')

register = template.Library()


def mycut(value, arg):
    return value.replace(arg, '')


register.filter('mycut', mycut)  # 注册装饰器的名字/单独注册


@register.filter(name='mylower')  # 直接在装饰器中以字符串的方式注册自定义装饰器的名字
def mylower(value):  # 给其传入的值不能缺失，否则将函数名字作为过滤器名字
    return value.lower()


@register.simple_tag(name='current_time1')  # 用于向Library注册实例，其后的name就是我们定义的类的名字
def current_time1(format_string):  # 用于在网页上展示时间
    print(format_string)  # 格式化字符串就是我们在H5中定义的现实格式：%Y 年 %m 月 %I 时 %M 分 %p
    return datetime.now().strftime(format_string)  #


@register.simple_tag(takes_context=True)
def current_time2(context):
    return datetime.now().strftime('format_string')


@register.inclusion_tag('show_tag.html')
def show_results1(value):
    li = ['Python', 'Java', 'C/C++']
    return {'choices': li}
