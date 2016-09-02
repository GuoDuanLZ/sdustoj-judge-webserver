from rest_framework_nested import routers

from .client_viewsets import ClientListViewSet, ClientDetailViewSet


router = routers.SimpleRouter()

router.register('clients', ClientListViewSet, base_name='clients')
router.register('clients', ClientDetailViewSet, base_name='clients')

urlpatterns = router.urls
