from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views import generic

from .forms import TaskCreationForm, TaskEditForm, AssignWorkerForm
from .models import Task, Worker


def index(request):
    user_tasks = Task.objects.filter(assignees=request.user.id)
    tasks = Task.objects.filter(is_completed=False)
    unique_priorities = tasks.values_list('priority', flat=True).distinct()
    task_counts = {
        priority: Task.objects.filter(priority=priority).filter(is_completed=False).count()
        for priority in unique_priorities
    }
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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


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
        task.complete_date = timezone.now()
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


@require_POST
@login_required
def join_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    task.assignees.add(request.user)

    return redirect('task_manager:task-detail', pk=task_id)


@require_POST
@login_required
def leave_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    task.assignees.remove(request.user)

    return redirect('task_manager:task-detail', pk=task_id)


@login_required
def completed_tasks_view(request):

    completed_tasks = Task.objects.filter(is_completed=True)

    context = {
        'completed_tasks': completed_tasks,
    }

    return render(request, "task_manager/archive_task_list.html", context)


@login_required
def create_task(request):
    priority = request.GET.get('priority', None)

    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user

            if priority is not None:
                task.priority = priority

            task.save()
            form.save_m2m()
            return redirect('task_manager:task-detail', pk=task.pk)

    else:

        initial_data = {'priority': priority} if priority is not None else {}
        form = TaskCreationForm(initial=initial_data)

    return render(request, 'task_manager/create_task.html', {'form': form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_manager:task-detail', pk=task.pk)
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'task_manager/edit_task.html', {'form': form, 'task': task})


@user_passes_test(lambda u: u.is_staff)
@login_required
def assign_worker_to_task(request):
    worker_id = request.GET.get('worker_id')

    if worker_id:
        worker = Worker.objects.get(id=worker_id)
        initial_data = {'worker': worker}
        form = AssignWorkerForm(initial=initial_data)
    else:
        form = AssignWorkerForm()

    if request.method == 'POST':
        form = AssignWorkerForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            worker = form.cleaned_data['worker']
            task.assignees.add(worker)
            return redirect('task_manager:task-detail', pk=task.pk)

    return render(request, 'task_manager/assign_worker_to_task.html', {'form': form})


def workers_list(request):
    workers_list = Worker.objects.all()
    paginator = Paginator(workers_list, 3)  # Вказуємо, скільки працівників показувати на одній сторінці

    page = request.GET.get('page')
    try:
        workers = paginator.page(page)
    except PageNotAnInteger:
        # Якщо номер сторінки не є цілим числом, відобразимо першу сторінку.
        workers = paginator.page(1)
    except EmptyPage:
        # Якщо номер сторінки за межами діапазону, відобразимо останню сторінку.
        workers = paginator.page(paginator.num_pages)

    context = {
        'workers': workers,
    }

    return render(request, "task_manager/worker_list.html", context)