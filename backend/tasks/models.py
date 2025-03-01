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
    
    def save(self, *args, **kwargs):
        if self.pk:  # Only log updates, not new tasks
            original = Task.objects.get(pk=self.pk)
            if original.status != self.status:
                History.objects.create(
                    title=self.title,
                    description=self.description,
                    due_date=self.due_date,
                    status=self.status,
                    task=self
                )
        super().save(*args, **kwargs)
    
class History(models.Model):
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
    
    saved_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)