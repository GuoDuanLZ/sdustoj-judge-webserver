from django.db.models import BigAutoField, CharField, DateTimeField, ManyToManyField
from utils.models import ModifyInfo, StatusMixin


class Client(ModifyInfo, StatusMixin):
    """
    使用此系统评测服务的客户端（Web教学端）的信息。
    """
    id = BigAutoField(primary_key=True)
    id_str = CharField(max_length=128, unique=True)
    full_name = CharField(max_length=128)
    last_update_time = DateTimeField()

    category = ManyToManyField('problem.Category', related_name='client')

    def __str__(self):
        return 'Client ' + str(id) + ': ' + str(self.full_name)
