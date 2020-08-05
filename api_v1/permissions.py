from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    """
    Allow only to Users who created this Favorite Query
    """

    def has_object_permission(self, request, view, obj):
        return obj.account == request.user
