from django.shortcuts import render
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializer import TaskSerializer
from .filters import TaskFilter
from .utils import get_similar_tasks, get_sequential_tasks

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

@api_view(['GET'])
def suggest_tasks(request):
    user_input = request.query_params.get('task_title', '')

    if not user_input:
        return Response({'error: Task title is required'}, status=400)
    
    similar_tasks = get_similar_tasks(user_input)
    sequential_tasks = get_sequential_tasks()

    return Response({
        'similar tasks': similar_tasks,
        'sequential tasks': sequential_tasks
    })