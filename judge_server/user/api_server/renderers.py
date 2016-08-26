from rest_framework.renderers import AdminRenderer


class APIRenderer(AdminRenderer):
    format = 'sdust'


class UserRenderer(APIRenderer):
    template = 'api_users.html'
