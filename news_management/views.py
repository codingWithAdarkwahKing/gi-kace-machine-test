from rest_framework import viewsets
from .models import Staff, Tag, Category, Report, ReportDesk
from .serializers import StaffSerializer, TagSerializer, CategorySerializer, ReportSerializer, ReportDeskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

class IsEditorOrAbove(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['editor', 'desk_head', 'zonal_editor', 'regional_editor', 'national_editor']

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated] 

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

class ReportDeskViewSet(viewsets.ModelViewSet):
    queryset = ReportDesk.objects.all()
    serializer_class = ReportDeskSerializer
    permission_classes = [IsEditorOrAbove]  
