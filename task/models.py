from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
# Create your models here.
# Database Model for Task data
class Task(models.Model):

    today = timezone.now

    OPTION_CHOICES = [
        ('Low', 'Option A'),
        ('Medium', 'Option B'),
        ('High', 'Option C'),
    ]
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name='tasks')
    title = models.TextField(default="Task Title")
    description = models.TextField()
    due_date = models.DateField(default=today)
    priority = models.CharField(choices=OPTION_CHOICES,default='Low',max_length=6)
    task_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
