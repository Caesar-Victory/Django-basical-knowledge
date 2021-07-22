# 开班典礼+web,Django介绍



# Django介绍

# 虚拟环境

# 创建Django项目

## 修改settings.py的设置

1，允许主机访问

```
ALLOWED_HOSTS = ['*']
```

2，安装look.apps

```
# Application definition

INSTALLED_APPS = [
    'look.apps.LookConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```



# git的使用



# 总结

Day01

介绍：是一个免费的开源web框架，排名第六；flask是一个轻量型框架，排名第七；

模式

MTV --- Model, Template , View

## 常用命令

```markdown
mmkvirtualenv -p python3 虚拟环境名称
退出虚拟环境
deactivate
删除虚拟环境
rmvirtualenv
使用和查看虚拟环境
workon
安装指定版本的Django
pip install django==2.1.10
查看已经安装的包
pip list
创建django项目（需要进入指定目录）
django-admin startproject 项目名称
创建一个子应用
cd tzlook
python manage.py startapp 子应用的名字[]
```

迁移数据库常用命令

```bash
python manage.py check  # 执行检查
python manage.py makemigrations look  # 指定迁移的app
python manage.py migrate  # 执行迁移
python manage.py sqlmigrate look 0001  # 打印迁移过程
```

配置pycharm

分别设置deployment和Interpret

运行项目

```
python manage.py runserver
```

修改允许主机

注册子应用

​	在settings.py中添加look.apps.AppConfig

## 模块解读

## 虚拟环境下的manage.py

```markdown
# 默认项目环境位置
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tzlook.settings')
```

## tzlook下的settings.py文件

```
# 整个项目文件的根目录
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

```

![image-20210509162137781](C:\Users\tylor\Documents\Baidu\Typora\Django第一课.assets\image-20210509162137781-1620548501494.png)

### 哈希密钥

```markdown
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!q)ot-pausiu3rxcfhe$cj&e!rbjdn$@9zfzn)&ss44a5bh*(v'
```

### 实时调试

```markdown
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

### 隐私方法，返回为空，代码仅为其中一部分

![image-20210509185619357](C:\Users\tylor\Documents\Baidu\Typora\Django第一课.assets\image-20210509185619357-1620557782267.png)

```python
class CsrfViewMiddleware(MiddlewareMixin):
    """
    Require a present and correct csrfmiddlewaretoken for POST requests that
    have a CSRF cookie, and set an outgoing CSRF cookie.

    This middleware should be used in conjunction with the {% csrf_token %}
    template tag.
    """
    # The _accept and _reject methods currently only exist for the sake of the
    # requires_csrf_token decorator.
    def _accept(self, request):
        # Avoid checking the request twice by adding a custom attribute to
        # request.  This will be relevant when both decorator and middleware
        # are used.
        request.csrf_processing_done = True
        return None
```

单词注释

```markdown
middleware
[uncountable] (computing计算机)
a layer of software in a computer between the operating system and applications that provides additional facilities not provided by the operating system中间件（允许不同程序协同工作）
```

![image-20210509190527038](C:\Users\tylor\Documents\Baidu\Typora\Django第一课.assets\image-20210509190527038-1620558328456.png)

### URL根目录---给settings提供接口进行访问

```python
ROOT_URLCONF = 'tzlook.urls'
```

### Django模板

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 可供添加自定义HTML文件
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 时区与语言

```python
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

### 默认数据库

```python
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### loook.views.py --- 模板渲染

位于子应用，也就是app中

```
from django.shortcuts import render

# Create your views here.
```

# 作业

1，上课笔记

2，下载一个截图软件

3，创建django项目

4，配置pycharm

5，创建子应用

6，注册子应用

7，运行项目文件