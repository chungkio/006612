from rest_framework.permissions import BasePermission

class AllowAnyPost(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated
