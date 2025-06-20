from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the profile
        return obj.owner == request.user

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for profile-related objects (skills, education, etc.)
    Only allows owners of the profile to edit related objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the profile
        return obj.profile.owner == request.user

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class CanEditOwnProfileOnly(permissions.BasePermission):
    """
    Permission that allows users to only edit their own profile
    but view all profiles
    """
    def has_permission(self, request, view):
        # Allow authenticated users to view all profiles
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow reading any profile
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow editing own profile
        return obj.owner == request.user