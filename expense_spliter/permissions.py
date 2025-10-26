from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True
        
        return obj.requester == request.user
    
class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True
        
        return obj.user == request.user
    
class IsAcceptingPersonOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True
        
        return obj.accepting_person == request.user
    
class IsParticipatingParty(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True
        
        return ((obj.person1 == request.user) or (obj.person2 == request.user))


