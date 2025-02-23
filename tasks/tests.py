from django.test import TestCase
from .models import Task
from .utils import get_similar_tasks, get_sequential_tasks
from unittest.mock import patch

# Create your tests here.
class TaskUtilsTests(TestCase):

    def setUp(self):
        self.task_1 = Task.objects.create(title="Project A Review", description="Review of Project A", status='completed', due_date="2025-02-25")
        self.task_2 = Task.objects.create(title="Project A Follow-up Meeting", description="Follow-up meeting for Project A", status='completed', due_date="2025-02-26")
        self.task_3 = Task.objects.create(title="Project B Testing", description="Testing for Project B", status='completed', due_date="2025-02-27")
        self.task_4 = Task.objects.create(title="Project C Finalization", description="Finalization of Project C", status='pending', due_date="2025-02-28")

    @patch('tasks.utils.SequenceMatcher')
    def test_get_similar_tasks(self, MockSequenceMatcher):
        """Test get_similar_tasks to find similar tasks by title"""
        mock_instance = MockSequenceMatcher.return_value
        mock_instance.ratio.return_value = 0.8
        
        task_title = "Project A Review"
        similar_tasks = get_similar_tasks(task_title)

        print(similar_tasks)
        
        self.assertIn("Project A Follow-up Meeting", similar_tasks)
        self.assertNotIn("Daily Stand Up", similar_tasks)


    def test_get_sequential_tasks(self):
        """Test get_sequential_tasks to find tasks completed in sequence"""
        sequential_tasks = get_sequential_tasks()

        print(sequential_tasks)

        self.assertIn(("Project A Review", "Project A Follow-up Meeting"), sequential_tasks)
        self.assertNotIn("Project B Testing", sequential_tasks)