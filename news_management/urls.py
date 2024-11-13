from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'staffs', views.StaffViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'report-desks', views.ReportDeskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
