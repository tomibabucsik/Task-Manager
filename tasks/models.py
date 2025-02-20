from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices= [
            ('pending', 'Pending'),
            ('in_progress', 'In progress'),
            ('completed', 'Completed')
        ],
        default='pending')
    
    def __str__(self):
        return self.title