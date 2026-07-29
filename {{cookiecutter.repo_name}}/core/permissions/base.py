from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_superuser or request.user.is_staff)


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user and getattr(request.user, "is_verified", False)


class CurrentUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_superuser
            or user.is_staff
            or obj.author == user.id
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.author == request.user.id
