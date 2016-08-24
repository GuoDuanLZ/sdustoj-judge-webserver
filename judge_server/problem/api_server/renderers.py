from rest_framework.renderers import AdminRenderer


class APIRenderer(AdminRenderer):
    format = 'sdust'


class MetaProblemListRenderer(APIRenderer):
    template = 'api_meta_problems.html'


class MetaProblemDetailRenderer(APIRenderer):
    template = 'api_meta_problem_detail.html'


class DescriptionListRenderer(APIRenderer):
    template = 'api_descriptions.html'


class DescriptionDetailRenderer(APIRenderer):
    template = 'api_description_detail.html'


class SampleListRenderer(APIRenderer):
    template = 'api_samples.html'


class SampleDetailRenderer(APIRenderer):
    template = 'api_sample_detail.html'


class TestDataListRenderer(APIRenderer):
    template = 'api_test_data.html'


class TestDataDetailRenderer(APIRenderer):
    template = 'api_test_data_detail.html'


class ProblemInMetaListRenderer(APIRenderer):
    template = 'api_problems_in_meta.html'


class ProblemInMetaDetailRenderer(APIRenderer):
    template = 'api_problem_detail_in_meta.html'


class ProblemListRenderer(APIRenderer):
    template = 'api_problems.html'


class ProblemTestDataRenderer(APIRenderer):
    template = 'api_test_data_problem.html'


class ProblemTestDataRelRenderer(APIRenderer):
    template = 'api_test_data_problem_relation.html'


class ProblemLimitRenderer(APIRenderer):
    template = 'api_limits.html'


class SubmissionListRenderer(APIRenderer):
    template = 'api_submissions.html'
