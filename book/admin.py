from django.contrib import admin

# Register your models here.
from .models import BookInfo, User
admin.site.register(BookInfo)
admin.site.register(User)
