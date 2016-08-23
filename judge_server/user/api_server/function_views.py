from rest_framework import viewsets, mixins, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

from .function_serializers import LoginSerializer


class AlreadyLogin(exceptions.PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Already login.')


class NotLogin(exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Not login.')


class UserDisabled(exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('User disabled.')


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise AlreadyLogin()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
            else:
                raise UserDisabled()
        else:
            raise AuthenticationFailed()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class Logout(viewsets.GenericViewSet):
    def list(self, request):
        if not request.user.is_authenticated():
            raise NotLogin()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
