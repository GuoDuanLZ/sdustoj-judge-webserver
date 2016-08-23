from rest_framework import filters
import django_filters

from ..models import Submission


class SubmissionFilter(filters.FilterSet):
    min_id = django_filters.NumberFilter(name='id', lookup_expr='gte')
    max_id = django_filters.NumberFilter(name='id', lookup_expr='lte')
    min_submit_time = django_filters.DateTimeFilter(name='submit_time', lookup_expr='gte')
    max_submit_time = django_filters.DateTimeFilter(name='submit_time', lookup_expr='lte')
    min_judge_time = django_filters.DateTimeFilter(name='judge_time', lookup_expr='gte')
    max_judge_time = django_filters.DateTimeFilter(name='judge_time', lookup_expr='lte')

    class Meta:
        model = Submission
        fields = ('id', 'problem',
                  'max_id', 'min_id',
                  'max_submit_time', 'min_submit_time',
                  'max_judge_time', 'min_judge_time',
                  'client', 'user', 'contest',
                  'finished', 'status')
