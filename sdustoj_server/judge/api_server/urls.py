from rest_framework_nested import routers

from .global_views import EnvironmentViewSet, EnvironmentDetailViewSet

router = routers.SimpleRouter()

router.register(r'environments', EnvironmentViewSet, base_name='environments')
router.register(r'environments', EnvironmentDetailViewSet, base_name='environments')

urlpatterns = []
urlpatterns += router.urls
