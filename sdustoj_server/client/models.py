from django.db import models
from utils.models import ModifyInfo, StatusMixin


class Client(ModifyInfo, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=64, unique=True)
    full_name = models.CharField(max_length=256)
