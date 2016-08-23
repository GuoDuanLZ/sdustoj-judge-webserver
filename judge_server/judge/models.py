from django.db.models import BigAutoField, CharField, ManyToManyField
from django.contrib.postgres.fields import JSONField
from utils.models import ModifyInfo, StatusMixin


class Environment(ModifyInfo, StatusMixin):
    """
    系统支持的编程环境信息，即提交程序可以交什么语言的程序。
    """
    eid = CharField(max_length=16, unique=True, help_text='供各Judge机决定编译方式的唯一标识符。', primary_key=True)
    language = CharField(max_length=32, help_text='阅读题目以及提交题目时对外显示的编程环境名称。')

    def __str__(self):
        return str(self.language)


class Machine(ModifyInfo, StatusMixin):
    id = BigAutoField(primary_key=True)

    name = CharField(max_length=32, unique=True)
    detail = CharField(max_length=256)

    settings = JSONField()

    cmd_queue = CharField(max_length=32)
    data_queue = CharField(max_length=32)

    environment = ManyToManyField(to=Environment, related_name='machine')
