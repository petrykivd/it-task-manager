from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Task, TaskType, Worker, Position


def index(request):
    tasks = Task.objects.filter(is_completed=False)
    unique_priorities = tasks.values_list('priority', flat=True).distinct()
    task_counts = {priority: Task.objects.filter(priority=priority).count() for priority in unique_priorities}
    context = {
        "tasks": tasks,
        "unique_priorities": unique_priorities,
        'task_counts': task_counts,
    }
    return render(
        request,
        "task_manager/index.html",
        context=context
    )


def logout_view(request):
    logout(request)
    return redirect("/")

