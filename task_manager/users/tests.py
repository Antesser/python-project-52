from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User

USER = {
    'username': 'lexion',
    'password': 'alexion',
}

USER_ONE = {
    'first_name': 'Pups',
    'last_name': 'Lovely',
    'username': 'pusanator228',
    'password1': 'iliketobealive',
    'password2': 'iliketobealive',
}
USER_TWO = {
    'first_name': 'Ahriman',
    'last_name': 'Ormuzd',
    'username': 'dark-descent',
    'password1': 'ourlifeisalie',
    'password2': 'ourlifeisalie',
}
USER_THREE = {
    'first_name': 'Lex',
    'last_name': 'Luthor',
    'username': 'bossman',
    'password1': 'no-regrets',
    'password2': 'no-regrets',
}


class UsersTest(TestCase):

    url_register = reverse_lazy('create_user')
    url_login = reverse_lazy('login')
    url_user_update = reverse_lazy('update_user', args=[1])
    url_user_delete = reverse_lazy('delete_user', args=[1])

    def setUp(self):
        self.user = User.objects.create_user(**USER)

    def test_user_register(self):
        initial_users_count = User.objects.count()
        self.client.post(self.url_register, data=USER_ONE)
        self.client.post(self.url_register, data=USER_TWO)
        self.assertEqual(User.objects.count(), initial_users_count + 2)

    def test_user_login(self):
        self.client.post(self.url_login, data=USER)
        auth_id = self.client.session['_auth_user_id']
        self.assertEqual(User.objects.get(pk=auth_id).username, 'lexion')

    def test_user_update(self):
        self.client.post(self.url_login, data=USER)
        self.client.post(self.url_user_update, data=USER_THREE)
        self.assertEqual(User.objects.get(pk=1).username, 'bossman')

    def test_user_delete(self):
        self.client.post(self.url_login, data=USER)
        self.client.post(self.url_user_delete)
        self.assertEqual(User.objects.count(), 0)
