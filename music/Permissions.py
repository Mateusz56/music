from rest_framework import permissions
from rest_framework.authtoken.models import Token


class UserDoubleAuth(permissions.BasePermission):
    message = 'Błędne hasło.'

    def has_permission(self, request, view):
        print(request.data)
        if request.method in permissions.SAFE_METHODS:
            return request.auth

        try:
            return Token.objects.get(key=request.auth).user.check_password(request.data.get('check_password'))
        except:
            return False
