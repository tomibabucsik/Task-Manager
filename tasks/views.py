from django.shortcuts import render
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializer import TaskSerializer
from .filters import TaskFilter

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['due_date', 'creation_date']
    ordering = ['due_date']

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer