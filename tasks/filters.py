import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Task._meta.get_field('status').choices)
    due_date = django_filters.DateFromToRangeFilter()
    creation_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['title', 'status', 'due_date', 'creation_date']