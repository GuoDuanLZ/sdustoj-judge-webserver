from rest_framework import permissions

from ..group_names import *


class InGroupPermission(permissions.BasePermission):
    group_name = None

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated():
            return False

        return user.groups.filter(name=self.group_name).exists()


class IsSiteAdmin(InGroupPermission):
    group_name = site_admin


class IsProblemAdmin(InGroupPermission):
    group_name = problem_admin


class ProblemAdminEditable(InGroupPermission):
    group_name = problem_admin

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if not user.is_authenticated():
                return False

            if user.groups.filter(name=problem_admin).exists() or user.groups.filter(name=category_admin).exists():
                return True
            else:
                return False
        else:
            return super().has_permission(request, view)


class IsCategoryAdmin(InGroupPermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated():
            return False

        if user.groups.filter(name=problem_admin).exists() or user.groups.filter(name=category_admin).exists():
            return True
        else:
            return False


class IsJudgeAdmin(InGroupPermission):
    group_name = judge_admin


class JudgeAdminEditable(InGroupPermission):
    group_name = judge_admin

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsClientAdmin(InGroupPermission):
    group_name = client_admin
