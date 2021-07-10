from django.db import models

# Create your models here.


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)  # 允许自定义ID
    d_name = models.CharField(max_length=20)  # 最大学院名称长度

    class Meta:
        db_table = 'department'

    def __str__(self):

        return self.d_name


class Student(models.Model):
    s_id = models.AutoField(primary_key=True)  # 允许自定义学生ID
    s_name = models.CharField(max_length=20)  # 学生名字的最大长度为20
    department = models.ForeignKey('Department', related_name='student', on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.s_name
