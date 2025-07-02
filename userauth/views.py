from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
from task.models import Task
from task.serializer import TaskSerializer

# For Swagger documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserRegistrationView(APIView):
    """
    Register a new user.

    Request body:
    {
        "username": "string",
        "password": "string"
    }

    Returns a success message if registration is successful.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            example={
                "username": "johndoe",
                "password": "securepassword123"
            }
        ),
        responses={201: openapi.Response('User created successfully')}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    Authenticate a user and return an access token.

    Request body:
    {
        "username": "string",
        "password": "string"
    }

    Returns an access token if credentials are valid.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            example={
                "username": "johndoe",
                "password": "securepassword123"
            }
        ),
        responses={202: openapi.Response('Access token')}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"access": str(AccessToken.for_user(user))}, status=status.HTTP_202_ACCEPTED)
        return Response("invalid credentials", status=status.HTTP_400_BAD_REQUEST)

class UserTasks(APIView):
    """
    Retrieve all tasks for the authenticated user.

    No request body required.

    Returns a list of tasks.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all tasks for the authenticated user.",
        responses={200: openapi.Response('List of tasks', TaskSerializer(many=True))}
    )
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


