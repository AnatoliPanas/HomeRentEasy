from rest_framework.permissions import BasePermission, SAFE_METHODS

from applications.users.choices.role_type import RoleType


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        print(request.user.role)
        return request.user.role in (RoleType.LESSOR.name,
                                     RoleType.MODERATOR.name,
                                     RoleType.ADMIN.name)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print(request.user,"--------",obj.owner)
            return request.user == obj.owner and request.user.role in (RoleType.LESSOR.name,
                                                                       RoleType.MODERATOR.name,
                                                                       RoleType.ADMIN.name)


class IsAdminOrAllowAny(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_staff
        return True
