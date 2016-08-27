from rest_framework.renderers import AdminRenderer, BaseRenderer


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


class TestDataListUploadRenderer(APIRenderer):
    template = 'api_test_data_upload.html'


class TestDataDetailRenderer(APIRenderer):
    template = 'api_test_data_detail.html'


class TestDataDetailUploadInRenderer(APIRenderer):
    template = 'api_test_data_detail_upload_in.html'


class TestDataDetailUploadOutRenderer(APIRenderer):
    template = 'api_test_data_detail_upload_out.html'


class ProblemInMetaListRenderer(APIRenderer):
    template = 'api_problems_in_meta.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        ret = super().get_context(data, accepted_media_type, renderer_context)
        print(renderer_context['view'])
        return ret


class ProblemInMetaDetailRenderer(APIRenderer):
    template = 'api_problem_detail_in_meta.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        ret = super().get_context(data, accepted_media_type, renderer_context)
        print(renderer_context['view'])
        return ret


class ProblemListRenderer(APIRenderer):
    template = 'api_problems.html'


class NewProblemRenderer(APIRenderer):
    template = 'api_new_problem.html'


class ProblemTestDataRenderer(APIRenderer):
    template = 'api_test_data_problem.html'


class ProblemTestDataRelRenderer(APIRenderer):
    template = 'api_test_data_problem_relation.html'


class ProblemLimitListRenderer(APIRenderer):
    template = 'api_limits.html'


class ProblemInvalidWordRenderer(APIRenderer):
    template = 'api_invalid_words.html'


class ProblemLimitDetailRenderer(APIRenderer):
    template = 'api_limits_detail.html'


class EmptyForm(BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        pass


class SubmissionListRenderer(APIRenderer):
    template = 'api_submissions.html'


class SubmissionDetailRenderer(APIRenderer):
    template = 'api_submission_detail.html'


class SubmissionJudgeRenderer(APIRenderer):
    template = 'api_submission_details.html'


class SubmissionMessageRenderer(APIRenderer):
    template = 'api_submission_message.html'


class SubmissionCodeInfoRenderer(APIRenderer):
    template = 'api_submission_code_info.html'


class SubmissionCodeRenderer(APIRenderer):
    template = 'api_submission_code.html'


class CategoryRenderer(APIRenderer):
    template = 'api_categories.html'


class CategoryNodeRenderer(APIRenderer):
    template = 'api_categorie_nodes.html'


class CategoryNodeProblemRenderer(APIRenderer):
    template = 'api_categorie_node_problems.html'


class CategoryNodeProblemRelationRenderer(APIRenderer):
    template = 'api_categorie_node_problem_relation.html'
