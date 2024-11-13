from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

@login_required(login_url='accounts:must_authenticate')
def home_view(request):
    return render(request, 'task_management/home.html')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)