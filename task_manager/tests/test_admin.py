from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import TaskType, Position, Worker

class TaskManagerAdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        admin_position = Position.objects.create(name="ADMIN")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpass",
            email="admin@example.com",
            position=admin_position,
        )

        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(username="worker", password="testpassword", position=self.position)
        self.task_type = TaskType.objects.create(name="Test Type")

    def test_task_type_admin(self):
        self.client.force_login(self.admin_user)

        url = reverse("admin:task_manager_tasktype_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.task_type.name)
