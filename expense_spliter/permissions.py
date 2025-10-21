from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if self.action == SAFE_METHODS:
            return True
        
        return obj.requester == request.user


