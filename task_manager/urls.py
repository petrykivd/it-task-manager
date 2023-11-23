from django.urls import path, include

from task_manager.views import (
    index,
    logout_view,
    TaskDetailView,
    mark_task_as_done,
    delete_task,
    WorkerDetailView,
    join_task,
    leave_task,
    completed_tasks_view, login_view
)

urlpatterns = [
    path("", index, name="index"),
    path("logout", logout_view, name="logout"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("mark_task_as_done/<int:task_id>/", mark_task_as_done, name="mark-task-as-done"),
    path("delete_task/<int:task_id>/", delete_task, name="delete-task"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("join_task/<int:task_id>/", join_task, name="join-task"),
    path("leave_task/<int:task_id>/", leave_task, name="leave-task"),
    path("archive/tasks_list/", completed_tasks_view, name="completed-tasks"),
    path("accounts/login/", login_view, name="login"),
]
app_name = "task_manager"
