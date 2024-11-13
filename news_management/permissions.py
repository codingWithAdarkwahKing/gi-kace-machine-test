from rest_framework import permissions

class IsZonalEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'zonal_editor'

class IsRegionalEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'regional_editor'

class IsNationalEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'national_editor'

class IsDeskHead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'desk_head'

class IsEditorOrAbove(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['editor', 'desk_head']
