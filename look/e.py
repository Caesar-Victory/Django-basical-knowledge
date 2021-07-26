from book.models import User

class UserMiddware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request 到达视图函数views之前执行的代码
        username = request.session.get('usernmae', '未登录')
        # 判断User表中是否存在该用户名
        user = User.objects.filter(username=username).first()  # 只抽取符合要求的第一个名字
        if user:
            setattr(request, 'myuser', user.username)
        else:
            setattr(request, 'myuser', '未登录')
        response = self.get_response
        return response