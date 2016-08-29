from rest_framework_nested import routers
from .submission_viewsets import StatusViewSet, ResultViewSet


router = routers.SimpleRouter()

router.register(r'status', StatusViewSet, base_name='status')
router.register(r'results', ResultViewSet, base_name='results')
urlpatterns = router.urls
