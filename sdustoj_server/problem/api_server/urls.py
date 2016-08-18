from rest_framework_nested import routers

from .meta_problem_viewsets import MetaProblemListViewSet, MetaProblemDetailViewSet
from .meta_problem_viewsets import DescriptionListViewSet, DescriptionDetailViewSet
from .meta_problem_viewsets import SampleListViewSet, SampleDetailViewSet
from .meta_problem_viewsets import TestDataListViewSet, TestDataDetailViewSet

from .problem_viewsets import ProblemListViewSet, ProblemDetailViewSet, ProblemReadOnlyViewSet
from .problem_viewsets import LimitListViewSet, LimitDetailViewSet
from .problem_viewsets import TestDataReadOnlyViewSet, TestDataRelationViewSet
from .problem_viewsets import DescriptionInProblemViewSet, SampleInProblemViewSet

from .category_viewsets import CategoryListViewSet, CategoryDetailViewSet
from .category_viewsets import NodeListViewSet, NodeDetailViewSet

from .submission_viewsets import SubmissionListViewSet, SubmissionDetailViewSet
from .submission_viewsets import SubmissionTestViewSet, SubmissionFilesViewSet
from .submission_viewsets import SubmissionCodeViewSet

router = routers.SimpleRouter()

# Meta Problem #########################################################################################################
router.register(r'meta-problems', MetaProblemListViewSet, base_name='meta-problems')
router.register(r'meta-problems', MetaProblemDetailViewSet, base_name='meta-problems')
meta_router = routers.NestedSimpleRouter(router, r'meta-problems', lookup='meta_problem')
# ----- Components --------------------------------------------------------------------------------
meta_router.register(r'descriptions', DescriptionListViewSet, base_name='descriptions')
meta_router.register(r'descriptions', DescriptionDetailViewSet, base_name='descriptions')
meta_router.register(r'samples', SampleListViewSet, base_name='samples')
meta_router.register(r'samples', SampleDetailViewSet, base_name='samples')
meta_router.register(r'test-data', TestDataListViewSet, base_name='test-data')
meta_router.register(r'test-data', TestDataDetailViewSet, base_name='test-data')

# Problem ##############################################################################################################
meta_router.register(r'problems', ProblemListViewSet, base_name='problems')
meta_router.register(r'problems', ProblemDetailViewSet, base_name='problems')
router.register(r'problems', ProblemReadOnlyViewSet, base_name='problems')
problem_router = routers.NestedSimpleRouter(router, r'problems', lookup='problem')
# ----- Component ---------------------------------------------------------------------------------
problem_router.register('limits', LimitListViewSet, base_name='limits')
problem_router.register('limits', LimitDetailViewSet, base_name='limits')
problem_router.register('test-data', TestDataReadOnlyViewSet, base_name='test-data')
problem_router.register('test-data-rel', TestDataRelationViewSet, base_name='test-data-rel')
problem_router.register('description', DescriptionInProblemViewSet, base_name='description')
problem_router.register('sample', SampleInProblemViewSet, base_name='sample')

# Category #############################################################################################################
router.register('categories', CategoryListViewSet, base_name='categories')
router.register('categories', CategoryDetailViewSet, base_name='categories')
cat_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
# ----- Component ---------------------------------------------------------------------------------
cat_router.register('nodes', NodeListViewSet, base_name='nodes')
cat_router.register('nodes', NodeDetailViewSet, base_name='nodes')

# Submission ###########################################################################################################
router.register('submissions', SubmissionListViewSet, base_name='submissions')
router.register('submissions', SubmissionDetailViewSet, base_name='submissions')
sub_router = routers.NestedSimpleRouter(router, r'submissions', lookup='submission')
sub_router.register('tests', SubmissionTestViewSet, base_name='test-info')
sub_router.register('files', SubmissionFilesViewSet, base_name='files')
sub_router.register('codes', SubmissionCodeViewSet, base_name='codes')


urlpatterns = []
urlpatterns += router.urls
urlpatterns += meta_router.urls
urlpatterns += problem_router.urls
urlpatterns += cat_router.urls
urlpatterns += sub_router.urls
