from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User

from .models import Task

USER = {
    'username': 'lexion',
    'password': 'alexion',
}

STATUS_ONE = {'name': 'This is out life'}
STATUS_TWO = {'name': 'Nothing stands on my way'}
STATUS_THREE = {'name': 'Starkiller'}

LABEL_ONE = {'name': 'Label_one'}
LABEL_TWO = {'name': 'Label_two'}
LABEL_THREE = {'name': 'Label_three'}

TASK_ONE = {
    'name': "We're victorious",
    'description': 'Not bad at all',
    'status': 1,
    'labels': 1,
}
TASK_TWO = {
    'name': 'Embrace the sun',
    'description': 'Smt went wrong',
    'status': 2,
    'labels': 2,
}
TASK_THREE = {
    'name': 'Taken for granted',
    'description': 'Fear me',
    'status': 3,
    'labels': 3,
}


class TasksTest(TestCase):

    url_login = reverse_lazy('login')
    url_status_create = reverse_lazy('create_status')
    url_label_create = reverse_lazy('create_label')
    url_task_create = reverse_lazy('create_task')
    url_task_update = reverse_lazy('update_task', args=[1])
    url_task_delete = reverse_lazy('delete_task', args=[1])

    def setUp(self):
        self.user = User.objects.create_user(**USER)
        self.client.post(self.url_login, data=USER)
        self.client.post(self.url_status_create, data=STATUS_ONE)
        self.client.post(self.url_status_create, data=STATUS_TWO)
        self.client.post(self.url_status_create, data=STATUS_THREE)
        self.client.post(self.url_label_create, data=LABEL_ONE)
        self.client.post(self.url_label_create, data=LABEL_TWO)
        self.client.post(self.url_label_create, data=LABEL_THREE)
        self.client.post(self.url_task_create, data=TASK_ONE)

    def test_task_read(self):
        task = Task.objects.get(id=1)
        self.assertEqual(task.name, "We're victorious")
        self.assertEqual(task.status.name, 'This is out life')
        self.assertEqual(task.description, 'Not bad at all')
        self.assertEqual(task.labels.all()[0].name, 'Label_one')

    def test_task_create(self):
        self.client.post(self.url_task_create, data=TASK_TWO)
        task = Task.objects.get(id=2)
        self.assertEqual(task.name, 'Embrace the sun')
        self.assertEqual(task.status.name, 'Nothing stands on my way')
        self.assertEqual(task.description, 'Smt went wrong')
        self.assertEqual(task.labels.all()[0].name, 'Label_two')

    def test_task_update(self):
        self.client.post(self.url_task_update, data=TASK_THREE)
        task = Task.objects.get(id=1)
        self.assertEqual(task.name, 'Taken for granted')
        self.assertEqual(task.status.name, 'Starkiller')
        self.assertEqual(task.description, 'Fear me')
        self.assertEqual(task.labels.all()[0].name, 'Label_three')

    def test_task_delete(self):
        self.client.post(self.url_task_delete)
        self.assertEqual(Task.objects.count(), 0)
