from django.shortcuts import render
from django.core.cache import cache
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, History
from .serializer import TaskSerializer, HistorySerializer
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
    cache.set('key', queryset, timeout=3600)


    def list(self, request, *args, **kwargs):
        cache_key = 'task_list'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response({
                'cache': True,
                'data': cached_data
            })
        
        queryset = self.get_queryset()
        serialized_data = TaskSerializer(queryset, many=True).data

        cache.set(cache_key, serialized_data, timeout=3600)

        return Response({
            'cache': False,
            'data': serialized_data
        })

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Log the update in History
        history = History.objects.create(
            title=instance.title,
            description=instance.description,
            creation_date=instance.creation_date,
            due_date=instance.due_date,
            status=instance.status,
            task=instance  # Link the history entry to the task
        )

        return Response(TaskSerializer(instance).data)
    
class HistoryListView(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

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