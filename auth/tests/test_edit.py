from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User


class AuthEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='test', password='pass')
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertJSONEqual(response.content, status_ok.content)

    def test_validation(self):
        url = '/auth/edit'
        c = self.client

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'password': 'some'})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'username': 'q'*31, 'password': 'pass'})
        self.assertJSONEqual(response.content, username_not_valid.content)

        response = c.post(url, {'email': 'admin_at_gmail.com', 'password': 'pass'})
        self.assertJSONEqual(response.content, email_not_valid.content)

        response = c.post(url, {'email': 'admin@gmail_dot_com', 'password': 'pass'})
        self.assertJSONEqual(response.content, email_not_valid.content)

    def test_exists(self):
        url = '/auth/edit'
        c = self.client

        User.objects.create_user(username='test2', password='secret', email='admin@gmail.com')

        response = c.post(url, {'username': 'test2', 'password': 'pass'})
        self.assertJSONEqual(response.content, username_already_exist.content)

        response = c.post(url, {'email': 'admin@gmail.com', 'password': 'pass'})
        self.assertJSONEqual(response.content, email_already_exist.content)

    def test_check_password(self):
        url = '/auth/edit'
        c = self.client

        response = c.post(url, {'username': 'test2', 'password': 'wrong_pass'})
        self.assertJSONEqual(response.content, auth_error.content)

    def test_edit(self):
        url = '/auth/edit'
        c = self.client

        response = c.post(url, {'username': 'test2', 'new_password': 'pass2', 'email': 'admin2@gmail.com',
                                'password': 'pass'})
        self.assertJSONEqual(response.content, status_ok.content)
        self.assertTrue(response.cookies)

        user = User.objects.filter(username='test2')
        self.assertTrue(user.exists())

        user = user[0]
        self.assertEqual(user.email, 'admin2@gmail.com')
        self.assertTrue(user.check_password('pass2'))
