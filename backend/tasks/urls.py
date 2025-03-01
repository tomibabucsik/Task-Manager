from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('suggest-tasks/', views.suggest_tasks, name='suggest_tasks'),
    path('history/', views.HistoryListView.as_view(), name='history_list'),
]