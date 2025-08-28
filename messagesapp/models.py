

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from tasksapp.models import Project

class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
