from collections import Counter
from django.db.models import Count
from difflib import SequenceMatcher
from .models import Task

def get_similar_tasks(task_title, threshold=0.6):
    all_tasks = Task.objects.values_list('title', flat=True)
    similar_tasks = []

    for existing_title in all_tasks:
        similarity = SequenceMatcher(None, task_title.lower(), existing_title.lower()).ratio()
        
        if similarity > threshold and existing_title.lower() != task_title.lower():
            similar_tasks.append(existing_title)

    return list(set(similar_tasks))

def get_sequential_tasks():
    completed_tasks = Task.objects.filter(status='completed').order_by('creation_date')
    sequential_tasks = []

    if len(completed_tasks) > 1:
        task_titles = [task.title for task in completed_tasks]

        for i in range(1, len(task_titles)):
            sequential_tasks.append((task_titles[i-1], task_titles[i]))

    return sequential_tasks
