from django.test import TestCase
from django.utils import timezone
from task_manager.forms import TaskCreationForm, TaskEditForm, AssignWorkerForm
from task_manager.models import Task, TaskType, Position, Worker
from django.contrib.auth import get_user_model


class TaskManagerFormsTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(username="worker", password="testpassword", position=self.position)
        self.task_type = TaskType.objects.create(name="Test Type")

    def test_task_creation_form(self):
        form_data = {
            "name": "New Test Task",
            "description": "Test description",
            "deadline": timezone.now() + timezone.timedelta(days=2),
            "priority": "medium",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }

        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_edit_form(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline=timezone.now() + timezone.timedelta(days=1),
            priority="urgent",
            task_type=self.task_type,
        )
        task.assignees.add(self.worker)

        form_data = {
            "name": "Edited Test Task",
            "description": "Edited description",
            "deadline": timezone.now() + timezone.timedelta(days=3),
            "priority": "critical",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }

        form = TaskEditForm(data=form_data, instance=task)
        self.assertTrue(form.is_valid())

    def test_assign_worker_form_invalid_task(self):
        worker2 = Worker.objects.create(username="worker2", password="testpassword", position=self.position)

        form_data = {
            "task": 999,
            "worker": worker2.id,
        }

        form = AssignWorkerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_assign_worker_form_invalid_worker(self):
        form_data = {
            "task": 1,
            "worker": 999,
        }

        form = AssignWorkerForm(data=form_data)
        self.assertFalse(form.is_valid())
