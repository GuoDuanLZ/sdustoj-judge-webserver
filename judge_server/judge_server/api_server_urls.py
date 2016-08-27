from django.conf.urls import url

from user.api_server import urls as user_urls
from judge.api_server import urls as judge_urls
from problem.api_server import urls as problem_urls

from api_web.views import api_homepage

urlpatterns = [
    url(r'^$', api_homepage, name='api_homepage'),
]
urlpatterns += user_urls.urlpatterns
urlpatterns += judge_urls.urlpatterns
urlpatterns += problem_urls.urlpatterns
