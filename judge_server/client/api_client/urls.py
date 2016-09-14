from rest_framework_nested import routers

from .client_viewsets import ClientViewSet, ProblemViewSet, CategoryViewSet, NodeViewSet, \
    CategoryProblemViewSet, NodeProblemViewSet, SubmissionViewSet


router = routers.SimpleRouter()
router.register('clients', ClientViewSet, base_name='clients')
client_router = routers.NestedSimpleRouter(router, 'clients', lookup='client')
client_router.register('problems', ProblemViewSet, base_name='problems')
client_router.register('categories', CategoryViewSet, base_name='categories')
client_router.register('submissions', SubmissionViewSet, base_name='submissions')

cat_router = routers.NestedSimpleRouter(client_router, 'categories', lookup='category')
cat_router.register('nodes', NodeViewSet, base_name='nodes')
cat_router.register('problems', CategoryProblemViewSet, base_name='problems')

node_router = routers.NestedSimpleRouter(cat_router, 'nodes', lookup='node')
node_router.register('problems', NodeProblemViewSet, base_name='problems')

urlpatterns = []
urlpatterns += router.urls
urlpatterns += client_router.urls
urlpatterns += cat_router.urls
urlpatterns += node_router.urls
