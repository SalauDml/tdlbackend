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
# Create your views here.

class SpecificTaskView(APIView):
    def get(self,request,id):
        try:
            task = Task.objects.get(id = id)
        except Task.DoesNotExist:
            raise(Http404("Does Not Exist"))
        serializer = TaskSerializer(task,many = False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class TaskView (APIView):
    # permission_classes = [permissions.AllowAny]
    def get(self,request):
        task = Task.objects.all()
        serializer = TaskSerializer(task,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post (self,request):
        # data = request.data
        serializer = TaskSerializer(data = request.data)
        # serializer.save(user = self.request.user)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response('Request received successfully', status=status.HTTP_201_CREATED)
        else:
            return Response(f'{serializer.errors}',status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request):
        id = self.request.query_params.get('id',"not available")
        task = Task.objects.get(id = id)
        serializer = TaskSerializer(task,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(f"${serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        try:
            # id = self.request.query_params.get('id',"not available")
            task = Task.objects.get(id = id)
        except Task.DoesNotExist:
            raise Http404("Does not Exist")
        task.delete()
        return Response({"message": "Deleted succesfully"},status=status.HTTP_204_NO_CONTENT)

class TokenView(APIView):
    permission_classes = [permissions.AllowAny]
    user = User.objects.first()
    def get(self,request):
        refresh = RefreshToken.for_user(self.user)
        return Response(str(refresh))

    




            



