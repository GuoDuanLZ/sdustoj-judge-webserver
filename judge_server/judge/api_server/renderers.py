from rest_framework.renderers import AdminRenderer


class APIRenderer(AdminRenderer):
    format = 'sdust'


class EnvironmentRenderer(APIRenderer):
    template = 'api_environments.html'


class MachineRenderer(APIRenderer):
    template = 'api_machines.html'
