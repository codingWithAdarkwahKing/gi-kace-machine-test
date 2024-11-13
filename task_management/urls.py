from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TaskViewSet

app_name = 'task_management'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('', include(router.urls)),
]