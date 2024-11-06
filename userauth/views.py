from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework import permissions
from task.models import Task
from task.serializer import TaskSerializer
# Create your views here.
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get (self,request):
        user = User.objects.all()
        serializer = UserSerializer(user, many = True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

    def post (self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post (self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            return Response({"access": str(AccessToken.for_user(user)), "refresh": str(RefreshToken.for_user(user))},status=status.HTTP_202_ACCEPTED)
        return Response("invalid credentials",status=status.HTTP_400_BAD_REQUEST)

class UserTasks (APIView):
    def get (self,request):
        tasks = Task.objects.all()
        tasks = tasks.filter(user = request.user)
        serializer = TaskSerializer (data =tasks,many = True)
        if serializer.is_valid():
            serializer.save
        return Response(data=serializer.data,status=status.HTTP_200_OK)


