from django.db import models
from django.contrib.auth.models import User




class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField( User, related_name="member_projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    TODO, INPROG, DONE = "TODO", "INPROG", "DONE"
    STATUS_CHOICES = [
        (TODO, "To-Do"),
        (INPROG, "In-Progress"),
        (DONE, "Done"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=TODO)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

