from django.apps import AppConfig
from django.db.models.signals import post_migrate

from . import group_names


def _check_group(group_name):
    from django.contrib.auth.models import Group
    field = Group.objects.filter(name=group_name).first()
    if field is None:
        group = Group(name=group_name)
        group.save()


def _check_groups():
    """
    检查用户组
    :return:
    """
    _check_group(group_names.site_admin)
    _check_group(group_names.problem_admin)
    _check_group(group_names.category_admin)
    _check_group(group_names.judge_admin)
    _check_group(group_names.client_admin)


def _check_user(username, first_name, last_name, password, *groups):
    from django.contrib.auth.models import User
    if not User.objects.filter(username=username).exists():
        print("创建用户：" + username)
        user = User(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        for group in groups:
            user.groups.add(group)


def _check_users():
    from django.contrib.auth.models import Group
    site_admin = Group.objects.filter(name=group_names.site_admin).first()
    problem_admin = Group.objects.filter(name=group_names.problem_admin).first()
    category_admin = Group.objects.filter(name=group_names.category_admin).first()
    judge_admin = Group.objects.filter(name=group_names.judge_admin).first()
    client_admin = Group.objects.filter(name=group_names.client_admin).first()
    groups = [site_admin, problem_admin, category_admin, judge_admin, client_admin]

    _check_user('korosensei', 'せんせー', '殺', 'big_boss', *groups)
    _check_user('kwy', 'Weiyi', 'Kong', '1352467000', *groups)
    _check_user('sdustoj', 'Judge', 'Online', 'sdust', *groups)


def _callback(sender, **kwargs):
    _check_groups()
    _check_users()


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        post_migrate.connect(_callback, sender=self)
