from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User


class AuthRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_validation(self):
        url = '/auth/register'
        c = self.client

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'username': 'q'*31, 'password': 'pass', 'email': 'admin2@gmail.com'})
        self.assertJSONEqual(response.content, username_not_valid.content)

        response = c.post(url, {'username': 'test2', 'password': 'pass', 'email': 'admin_at_gmail.com'})
        self.assertJSONEqual(response.content, email_not_valid.content)

        response = c.post(url, {'username': 'test2', 'password': 'pass', 'email': 'admin@gmail_dot_com'})
        self.assertJSONEqual(response.content, email_not_valid.content)

    def test_register(self):
        url = '/auth/register'
        c = self.client

        response = c.post(url, {'username': 'test', 'password': 'pass', 'email': 'admin@gmail.com'})
        self.assertJSONEqual(response.content, status_ok.content)

        user = User.objects.filter(username='test')
        self.assertTrue(user.exists())

        user = user[0]
        self.assertEqual(user.username, 'test')
        self.assertTrue(user.check_password('pass'))
        self.assertEqual(user.email, 'admin@gmail.com')

        response = c.post(url, {'username': 'test', 'password': 'pass', 'email': 'admin2@gmail.com'})
        self.assertJSONEqual(response.content, username_already_exist.content)

        response = c.post(url, {'username': 'test2', 'password': 'pass', 'email': 'admin@gmail.com'})
        self.assertJSONEqual(response.content, email_already_exist.content)
