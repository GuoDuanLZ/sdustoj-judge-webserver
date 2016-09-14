from judge.api_client import urls as judge_urls
from client.api_client import urls as client_urls

urlpatterns = []
urlpatterns += judge_urls.urlpatterns
urlpatterns += client_urls.urlpatterns
