from utils.filters import ResourceFilter

from ..models import Problem, Limit


resource_fields = ResourceFilter.resource_fields


class ProblemFilter(ResourceFilter):
    class Meta:
        model = Problem
        fields = resource_fields + ('id',)


class LimitFilter(ResourceFilter):
    class Meta:
        model = Limit
        fields = resource_fields + ('id',)
