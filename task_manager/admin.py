from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, TaskType, Position, Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'position')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'position'),
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
