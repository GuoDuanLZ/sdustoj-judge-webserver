import django_filters
from rest_framework import filters

from django.contrib.auth.models import User


class UserFilter(filters.FilterSet):
    date_joined_gte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gte')
    date_joined_lte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='lte')
    last_login_gte = django_filters.DateTimeFilter(name='last_login', lookup_expr='gte')
    last_login_lte = django_filters.DateTimeFilter(name='last_login', lookup_expr='lte')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active',
                  'date_joined_gte', 'date_joined_lte',
                  'last_login_gte', 'last_login_lte')
