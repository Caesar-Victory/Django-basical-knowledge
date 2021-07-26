from django.contrib import admin
# from look.models import
# Register your models here.
from .models import Student, Department
admin.site.register(Student)
admin.site.register(Department)