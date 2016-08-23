from utils.filters import ResourceFilter

from ..models import MetaProblem, Description, Sample


resource_fields = ResourceFilter.resource_fields


class MetaProblemFilter(ResourceFilter):
    class Meta:
        model = MetaProblem
        fields = resource_fields = ('id',)


class DescriptionFilter(ResourceFilter):
    class Meta:
        model = Description
        fields = resource_fields = ('id',)


class SampleFilter(ResourceFilter):
    class Meta:
        model = Sample
        fields = resource_fields = ('id',)
