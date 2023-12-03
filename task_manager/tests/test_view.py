from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from task_manager.models import Task, TaskType, Position, Worker
from django.contrib.auth import get_user_model

class TaskManagerViewsTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword", position=self.position)
        self.task_type = TaskType.objects.create(name="Test Type")
        self.worker = Worker.objects.create(username="worker", password="testpassword", position=self.position)

        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline=timezone.now() + timezone.timedelta(days=1),
            priority="urgent",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker)

    def test_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/index.html")

    def test_task_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_manager:task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_detail.html")

    def test_create_task_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_manager:create-task"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/create_task.html")

        response = self.client.post(reverse("task_manager:create-task"), {
            "name": "New Test Task",
            "description": "New Test Description",
            "deadline": timezone.now() + timezone.timedelta(days=2),
            "priority": "medium",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        })
        self.assertEqual(response.status_code, 302)

        new_task = Task.objects.get(name="New Test Task")
        self.assertIsNotNone(new_task)
