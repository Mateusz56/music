from rest_framework import permissions
from rest_framework.authtoken.models import Token


class UserDoubleAuth(permissions.BasePermission):
    message = 'Błędne hasło.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.auth

        try:
            return Token.objects.get(key=request.auth).user.check_password(request.data.get('check_password'))
        except:
            return False


class AlbumPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:

            user = Token.objects.get(key=request.auth).user
            return user in obj.owners
        except:
            return False


class AlbumInvitationAuth(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS\
                    or getattr(obj, 'user', None) == request.user\
                    or request.user in getattr(obj, 'owners', []).all():
                return True
        except:
            return False
        return False


class IsAuthorPermissionOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.user == getattr(obj, 'author', None):
                return True
        except:
            return False
        return False


class AlbumPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if obj.public or request.user in getattr(obj, 'owners', []).all():
                return True
        except:
            return False
        return False