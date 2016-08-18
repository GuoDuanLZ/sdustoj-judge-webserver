import django_filters
from rest_framework import filters

from ..models import Submission, SubmissionTest, SubmissionCode


class SubmissionFilter(filter.FilterSet):
    min_id = django_filters.NumberFilter(name="id", lookup_expr='gte')
    max_id = django_filters.NumberFilter(name="id", lookup_expr='lte')
    class Meta:
        model =Submission
        fields=('id','result','min_id','max_id','environment',)


class SubmissionTestFilter(filter.FilterSet):
    class Meta:
        model =SubmissionTest
        fields=()

class SubmissionCodeFilter(filter.FilterSet):
    class Meta:
        model =SubmissionCode
        fields=()