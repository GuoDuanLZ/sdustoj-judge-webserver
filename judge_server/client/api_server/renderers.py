from rest_framework.renderers import AdminRenderer, BaseRenderer


class APIRenderer(AdminRenderer):
    format = 'sdust'


class ClientRenderer(APIRenderer):
    template = 'api_clients.html'
