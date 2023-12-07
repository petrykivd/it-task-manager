from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}  ({self.position})"

    # def get_absolute_url(self):
    #     return reverse("")


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("asap", "ASAP (As Soon As Possible)"),
        ("medium", "Medium"),
        ("critical", "Critical"),

    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=30,
                                choices=PRIORITY_CHOICES,
                                default="medium")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    complete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return f"Task: {self.name}, type: ({self.task_type})"

    def is_task_overdue(self):
        if self.deadline < timezone.now():
            return True
        return False
