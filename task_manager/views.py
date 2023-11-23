from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Task, TaskType, Worker, Position


def index(request):
    user_tasks = Task.objects.filter(assignees=request.user.id)

    tasks = Task.objects.filter(is_completed=False)

    unique_priorities = tasks.values_list('priority', flat=True).distinct()
    task_counts = {priority: Task.objects.filter(priority=priority).count() for priority in unique_priorities}
    context = {
        "tasks": tasks,
        "unique_priorities": unique_priorities,
        "task_counts": task_counts,
        "user_tasks": user_tasks,
    }

    return render(
        request,
        "task_manager/index.html",
        context=context
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


@login_required
def mark_task_as_done(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        task.is_completed = True
        task.save()
        messages.success(request, 'Task marked as done successfully.')
    except Task.DoesNotExist:
        messages.error(request, 'Task not found.')

    return redirect('/')


@login_required()
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        tasks = Task.objects.filter(assignees=worker)
        context['tasks'] = tasks
        return context
