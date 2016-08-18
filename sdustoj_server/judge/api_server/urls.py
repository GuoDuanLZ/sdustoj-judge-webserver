from rest_framework_nested import routers

from .global_views import EnvironmentViewSet, EnvironmentDetailViewSet
from .machine_viewsets import MachineListViewSet, MachineDetailViewSet

router = routers.SimpleRouter()

router.register(r'environments', EnvironmentViewSet, base_name='environments')
router.register(r'environments', EnvironmentDetailViewSet, base_name='environments')

router.register(r'machines', MachineListViewSet, base_name='machines')
router.register(r'machines', MachineDetailViewSet, base_name='machines')

urlpatterns = []
urlpatterns += router.urls
