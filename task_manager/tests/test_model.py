from django.test import TestCase
from django.utils import timezone
from task_manager.models import Task, TaskType, Position, Worker
from django.contrib.auth import get_user_model

class TaskManagerModelsTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(username="worker", password="testpassword", position=self.position)
        self.task_type = TaskType.objects.create(name="Test Type")

    def test_task_model(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline=timezone.now() + timezone.timedelta(days=1),
            priority="urgent",
            task_type=self.task_type,
        )
        task.assignees.add(self.worker)

        self.assertEqual(str(task), f"Task: {task.name}, type: ({task.task_type})")
        self.assertFalse(task.is_task_overdue())
        self.assertEqual(task.assignees.count(), 1)

    def test_task_type_model(self):
        task_type = TaskType.objects.create(name="New Type")
        self.assertEqual(str(task_type), "New Type")

    def test_position_model(self):
        position = Position.objects.create(name="New Position")
        self.assertEqual(str(position), "New Position")

    def test_worker_model(self):
        worker = Worker.objects.create(username="new_worker", password="testpassword", position=self.position)
        self.assertEqual(str(worker), f"{worker.first_name} {worker.last_name}  ({worker.position})")
