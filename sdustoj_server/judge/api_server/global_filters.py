from utils.filters import ResourceFilter

from ..models import Environment


resource_fields = ResourceFilter.resource_fields


class EnvironmentFilter(ResourceFilter):
    class Meta:
        model = Environment
        fields = resource_fields + ('eid', 'language')
