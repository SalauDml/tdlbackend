from django.urls import path,include
from .views import TaskView,TokenView,SpecificTaskView
urlpatterns = [
    path('',TaskView.as_view()),
    path('<int:id>',SpecificTaskView.as_view()),
    path('token',TokenView.as_view())
]