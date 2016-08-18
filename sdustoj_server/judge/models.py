from django.db import models
from utils.models import ModifyInfo,StatusMixin


class Environment(ModifyInfo, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    eid = models.CharField(max_length=16, unique=True, help_text='供各Judge机决定编译方式的唯一标识符。')
    language = models.CharField(max_length=32, help_text='阅读题目以及提交题目时对外显示的编程环境名称。')
