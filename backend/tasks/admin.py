from django.contrib import admin
from .models import Task, History

# Register your models here.
admin.site.register(Task)
admin.site.register(History)