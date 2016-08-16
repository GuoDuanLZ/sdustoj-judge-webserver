from user.api_server import urls as user_urls
from judge.api_server import urls as judge_urls
from problem.api_server import urls as problem_urls

urlpatterns = []
urlpatterns += user_urls.urlpatterns
urlpatterns += judge_urls.urlpatterns
urlpatterns += problem_urls.urlpatterns
