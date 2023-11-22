from django.urls import path, include

from task_manager.views import index, logout_view

urlpatterns = [
    path("", index, name="index"),
    path("logout", logout_view, name="logout")
]

app_name = "task_manager"
