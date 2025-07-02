from django.shortcuts import render
from rest_framework.views import APIView
from .models import Task
from .serializer import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.contrib.auth.models import User
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

AUTH_HEADER = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <access_token>",
    type=openapi.TYPE_STRING,
    required=True
)
    
class TaskView(APIView):
    """
    List all tasks, create, update, or delete a task.
    """
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all tasks belonging to the authenticated user. Optional query parameters: status, priority, due_date.",
        manual_parameters=[
            AUTH_HEADER,
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter tasks by completion status (true/false)",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
            openapi.Parameter(
                'priority',
                openapi.IN_QUERY,
                description="Filter tasks by priority (Low, Medium, High)",
                type=openapi.TYPE_STRING,
                enum=['Low', 'Medium', 'High'],
                required=False
            ),
            openapi.Parameter(
                'due_date',
                openapi.IN_QUERY,
                description="Filter tasks due before this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date',
                required=False
            ),
        ],
        responses={200: openapi.Response('List of tasks', TaskSerializer(many=True))}
    )
    def get(self, request):
        task = Task.objects.all().filter(user=request.user)
        state = request.query_params.get('status', None)
        priority = request.query_params.get('priority', None)
        due_date = request.query_params.get('due_date', None)
        if state is not None:
            task = task.filter(task_complete=status.lower() == 'true')
        if priority:
            task = task.filter(priority=priority)
        if due_date:
            task = task.filter(due_date__lt=due_date)

        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new task.",
        manual_parameters=[AUTH_HEADER],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description', 'priority', 'task_complete', 'due_date'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the task'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the task'),
                'priority': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Priority of the task (Low, Medium, High)',
                    enum=['Low', 'Medium', 'High']
                ),
                'task_complete': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the task complete?'),
                'due_date': openapi.Schema(type=openapi.TYPE_STRING, description='Due date in YYYY-MM-DD format'),
            },
            example={
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs",
                "priority": "Medium",
                "task_complete": False,
                "due_date": "2025-07-10"
            }
        ),
        responses={201: openapi.Response('Task created successfully')}
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response('Request received successfully', status=status.HTTP_201_CREATED)
        else:
            return Response(f'{serializer.errors}', status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a task. Provide the task ID and any fields to update.",
        manual_parameters=[AUTH_HEADER],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task to update'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the task'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the task'),
                'priority': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Priority of the task (Low, Medium, High)',
                    enum=['Low', 'Medium', 'High']
                ),
                'task_complete': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the task complete?'),
                'due_date': openapi.Schema(type=openapi.TYPE_STRING, description='Due date in YYYY-MM-DD format'),
            },
            example={
                "id": 1,
                "title": "Buy groceries and fruits",
                "description": "Milk, Bread, Eggs, Apples",
                "priority": "High",
                "task_complete": True,
                "due_date": "2025-07-12"
            }
        ),
        responses={202: openapi.Response('Task updated successfully')}
    )
    def patch(self, request):
        try:
            task = Task.objects.get(id=request.data.get('id'))
        except Task.DoesNotExist:
            raise Http404("Does not Exist")
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(f"{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a task by its ID. Provide the task ID in the request body.",
        manual_parameters=[AUTH_HEADER],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task to delete'),
            },
            example={
                "id": 1
            }
        ),
        responses={204: openapi.Response('Task deleted successfully')}
    )
    def delete(self, request):
        try:
            task = Task.objects.get(id=request.data.get('id'))
        except Task.DoesNotExist:
            raise Http404("Does not Exist")
        task.delete()
        return Response({"message": "Deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)











