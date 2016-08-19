from django.db import models
from utils.models import ModifyInfo, StatusMixin

from django.contrib.postgres import fields as pg_fields


class Environment(ModifyInfo, StatusMixin):
    eid = models.CharField(max_length=16, unique=True, help_text='供各Judge机决定编译方式的唯一标识符。', primary_key=True)
    language = models.CharField(max_length=32, help_text='阅读题目以及提交题目时对外显示的编程环境名称。')

    def __str__(self):
        return str(self.language)


class Machine(ModifyInfo, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=32, unique=True)
    detail = models.CharField(max_length=256)

    settings = pg_fields.JSONField()

    environment = models.ManyToManyField(to=Environment, related_name='machine')
