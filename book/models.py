from django.db import models

# Create your models here.
"""
继承自谁models
模型类和数据库关系
属性和表字段对应的关系
"""


class User(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()  # 年龄一般均为1-100,所以指定长度没有太大的意义,但这可能成为一个攻击点
    gender = models.BooleanField()

    class Meta:
        db_table = 'user'  # 指定表名
        managed = True  # https://www.cnblogs.com/michealjy/p/14018517.html

    def __str__(self):
        return self.name


class BookInfo(models.Model):
    name = models.CharField(max_length=26)  # 一个数字两个字符，所以尽量用偶数
    pub_date = models.DateField(verbose_name='发布日期', null=True)
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    comment_count = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    book = models.ForeignKey('User', on_delete=models.CASCADE)  # 级联删除，一删除则多也会删除---连根拔起

    class Meta:
        db_table = 'bookinfo'

    def __str__(self):
        return self.name
