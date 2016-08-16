from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^password/',persontopassword, name='persontopassword'),
    url(r'^$', homepage, name='homepage'),
    url(r'^home/', homepage, name='homepage'),
    url(r'^login/', sign_in, name='sign_in'),
    url(r'^personal/', personal, name='personal'),
    url(r'^table/', table_example, name='table'),
    url(r'^passwordSET/',ajax_password,name='ajax_password'),
    url(r'^userinfo/',ajax_user, name='ajax_user'),
    url(r'table_example/',tablerender,name='table'),
    url(r'problem/', problemManager, name='problem'),
    url(r'problem-add/',problemAdd,name='problem-add'),
    url(r'problem-modify',problemModify,name='problem-modify'),
    url(r'problem-detail',problemDetail,name='problem-detail'),
]
