from django.shortcuts import render
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
dc = {'a':1, 'b':2}
def index_4(request):
    return render(request, 'tzlook/index.html',
                  context = {'books_name': 'python',
                             'hello':'hello',
                             'fruits_say':ap.say,
                             'fruits':ap,
                             'list':ls,
                             'dict':dc,
                             })
