from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserTasks
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register',UserRegistrationView.as_view()),
    path('login',UserLoginView.as_view()),
    path('tasks',UserTasks.as_view())
]