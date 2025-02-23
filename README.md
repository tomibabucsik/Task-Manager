# Task-Manager

Setup Instructions
1. Clone the repository: git clone https://github.com/tomibabucsik/Task-Manager.git
2. Create a virtual enviroment: python -m venv venv ; then activate it: venv\Scripts\activate
3. Install dependencies: pip install -r requirements.txt
4. Apply Database Migrations: python manage.py migrats
5. Create a superuser to access Django Admin panel: python manage.py createsuperuser
6. Run the development server: python manage.py runserver

API docmentation
Endpoints:

1. List and Create Tasks
URL: /api/tasks/
Method: GET (list all tasks) / POST (create a new task)
Request Body (for POST):
{
    "title": "Task Title",
    "description": "Task Description",
    "due_date": "YYYY-MM-DD",
    "status": "pending"
}

Response (for GET):
{
     "id": 1,
     "title": "Task Title",
     "description": "Task Description",
     "status": "pending",
     "due_date": "YYYY-MM-DD"
}

2. Retrieve, Update, and Delete Task
URL: /api/tasks/{id}/
Method: GET (retrieve a task) / PUT (update a task) / DELETE (delete a task)

3. Suggest Similar Tasks
URL: /api/suggest-tasks/
Method: GET
Query Parameters: task_title (title of the task for which similar tasks are to be suggested)
Example: GET http://127.0.0.1:8000/api/suggest-tasks/?task_title=Project%20A%20Review
Response:
{
    "similar tasks": [
        "Project B Testing",
        "Project A Follow-up Meeting"
    ],
    "sequential tasks": [
        ["Project A Review", "Project A Follow-up Meeting"]
    ]
}

5. Filtering and Sorting
The TaskListCreateView supports filtering tasks by status and sorting them by creation date or due date using query parameters.
To filter by status, use status={value} (e.g., /api/tasks/?status=completed).
To sort tasks, use the ordering query parameter (ordering=due_date or ordering=-due_date for descending order).

Design Decisions
1. Task Data Model
The Task model includes fields such as title, description, status, and due_date to capture essential task information.
The status field has three choices: pending, in_progress, and completed.

2. Similarity Calculation (SequenceMatcher)
The similarity between task titles is calculated using the SequenceMatcher from Python's difflib module, with a threshold of 0.8 to determine whether two tasks are considered similar.
"Similar tasks" endpoint is used for this.

3. Sequential Task Calculation
Sequential tasks are determined based on the assumption that tasks marked as completed follow each other in a logical order.
Tasks that are marked as completed are evaluated in the order they were completed (based on their due_date), and pairs of tasks that are completed consecutively are flagged as sequential.

4. Testing
Unit tests are written using Django's TestCase framework to verify the core functionalities of the application, including task creation, task retrieval, task suggestions, and task sequence detection.
