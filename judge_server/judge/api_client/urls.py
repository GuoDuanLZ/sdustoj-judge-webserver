from rest_framework_nested import routers

from .global_viewsets import EnvironmentViewSet


router = routers.SimpleRouter()

router.register('environments', EnvironmentViewSet, base_name='environments')

urlpatterns = router.urls
