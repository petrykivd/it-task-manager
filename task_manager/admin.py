from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, TaskType, Position, Worker

admin.site.register(Task)

admin.site.register(TaskType)

admin.site.register(Position)

admin.site.register(Worker)
