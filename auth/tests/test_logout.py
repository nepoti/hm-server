from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User


class AuthLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_anonymous(self):
        url = '/auth/logout'
        url_login = '/auth/login'
        c = self.client

        response = c.post(url, {})
        self.assertJSONEqual(response.content, status_ok.content)

        response = c.post(url_login, {'cookies': 'true'})
        self.assertJSONEqual(response.content, auth_error.content)

    def test_logout_user(self):
        url = '/auth/logout'
        url_login = '/auth/login'
        c = self.client

        User.objects.create_user(username='test', password='pass')

        response = c.post(url_login, {'username': 'test', 'password': 'pass'})
        self.assertTrue(response.cookies)

        response = c.post(url, {})
        self.assertJSONEqual(response.content, status_ok.content)

        response = c.post(url_login, {'cookies': 'true'})
        self.assertJSONEqual(response.content, auth_error.content)

        response = c.post(url, {})
        self.assertJSONEqual(response.content, status_ok.content)
