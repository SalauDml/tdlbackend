from django.urls import path,include
from .views import TaskView
urlpatterns = [
    path('',TaskView.as_view()),
]