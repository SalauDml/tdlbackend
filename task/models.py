from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name='tasks')
    title = models.TextField(default="Task Title")
    description = models.TextField()
    task_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
