from rest_framework_nested import routers

from .meta_problem_viewsets import MetaProblemListViewSet, MetaProblemDetailViewSet
from .meta_problem_viewsets import DescriptionListViewSet, DescriptionDetailViewSet
from .meta_problem_viewsets import SampleListViewSet, SampleDetailViewSet
from .meta_problem_viewsets import TestDataListViewSet, TestDataDetailViewSet
from .meta_problem_viewsets import TestInFileViewSet, TestOutFileViewSet
from .meta_problem_viewsets import TestFileUploadViewSet, TestInFileUploadViewSet, TestOutFileUploadViewSet

from .problem_viewsets import ProblemListViewSet, ProblemDetailViewSet, ProblemReadOnlyViewSet, NewProblemViewSet, \
    SpecialJudgeListViewSet, SpecialJudgeDetailViewSet
from .problem_viewsets import LimitListViewSet, LimitDetailViewSet
from .problem_viewsets import InvalidWordListViewSet
from .problem_viewsets import TestDataReadOnlyViewSet, TestDataRelationViewSet
from .problem_viewsets import DescriptionInProblemViewSet, SampleInProblemViewSet
from .problem_viewsets import NodeProblemListViewSet, NodeProblemDetailViewSet

from .submission_viewsets import SubmissionListViewSet, SubmissionDetailViewSet
from .submission_viewsets import SubmissionMessageViewSet, SubmissionMoreDetailViewSet, SubmissionCodeInfoViewSet
from .submission_viewsets import SubmissionCodeViewSet

from .category_viewsets import CategoryListViewSet, CategoryDetailViewSet
from .category_viewsets import NodeListViewSet, NodeDetailViewSet
from .category_viewsets import ProblemCategoryNodeViewSet, ProblemCategoryNodeDetailViewSet

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
meta_router.register(r'test-data-files', TestFileUploadViewSet, base_name='in_file')
meta_router.register(r'test-data-in', TestInFileUploadViewSet, base_name='test-data-in')
meta_router.register(r'test-data-out', TestOutFileUploadViewSet, base_name='test-data-out')
test_router = routers.NestedSimpleRouter(meta_router, r'test-data-files', lookup='test')
test_router.register(r'in', TestInFileViewSet, base_name='in_file')
test_router.register(r'out', TestOutFileViewSet, base_name='in_file')

# Problem ##############################################################################################################
meta_router.register(r'problems', ProblemListViewSet, base_name='problems')
meta_router.register(r'problems', ProblemDetailViewSet, base_name='problems')
router.register(r'problems', ProblemReadOnlyViewSet, base_name='problems')
router.register(r'new-problems', NewProblemViewSet, base_name='new_problems')
problem_router = routers.NestedSimpleRouter(router, r'problems', lookup='problem')
# ----- Component ---------------------------------------------------------------------------------
problem_router.register(r'limits', LimitListViewSet, base_name='limits')
problem_router.register(r'limits', LimitDetailViewSet, base_name='limits')
problem_router.register(r'invalid-words', InvalidWordListViewSet, base_name='invalid-words')
problem_router.register(r'test-data', TestDataReadOnlyViewSet, base_name='test-data')
problem_router.register(r'test-data-rel', TestDataRelationViewSet, base_name='test-data-rel')
problem_router.register(r'description', DescriptionInProblemViewSet, base_name='description')
problem_router.register(r'sample', SampleInProblemViewSet, base_name='sample')

# Submission ###########################################################################################################
router.register(r'submissions', SubmissionListViewSet, base_name='submissions')
router.register(r'submissions', SubmissionDetailViewSet, base_name='submissions')
router.register(r'submission-messages', SubmissionMessageViewSet, base_name='submission-messages')
router.register(r'submission-details', SubmissionMoreDetailViewSet, base_name='submission-details')
router.register(r'submission-code-info', SubmissionCodeInfoViewSet, base_name='submission-code-info')
code_router = routers.NestedSimpleRouter(router, r'submission-code-info', lookup='info')
code_router.register(r'codes', SubmissionCodeViewSet, base_name='submission-codes')

# Category #############################################################################################################
router.register('categories', CategoryListViewSet, base_name='categories')
router.register('categories', CategoryDetailViewSet, base_name='categories')
cat_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
# ----- Component ---------------------------------------------------------------------------------
cat_router.register('nodes', NodeListViewSet, base_name='nodes')
cat_router.register('nodes', NodeDetailViewSet, base_name='nodes')
# router.register(r'nodes', NodeListViewSet, base_name='nodes')
router.register(r'nodes', NodeDetailViewSet, base_name='nodes')
nod_router = routers.NestedSimpleRouter(router, r'nodes', lookup='node')
nod_router.register(r'problems', NodeProblemListViewSet, base_name='problems')
nod_router.register(r'problems', NodeProblemDetailViewSet, base_name='problems')
nod_router.register('problem-rel', ProblemCategoryNodeViewSet, base_name='node-rel')
nod_router.register('problem-rel', ProblemCategoryNodeDetailViewSet, base_name='node-rel')
# SpecialJudge #########################################################################################################
problem_router.register(r'special-judge', SpecialJudgeListViewSet, base_name='special-juddge')
problem_router.register(r'special-judge', SpecialJudgeDetailViewSet, base_name='special-juddge')


urlpatterns = []
urlpatterns += router.urls
urlpatterns += meta_router.urls
urlpatterns += test_router.urls
urlpatterns += problem_router.urls
urlpatterns += code_router.urls
urlpatterns += cat_router.urls
urlpatterns += nod_router.urls
