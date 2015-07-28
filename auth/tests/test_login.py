from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User


class AuthLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='test', password='pass')

    def test_login(self):
        url = '/auth/login'
        c = self.client

        response = c.post(url, {'username': 'test', 'password': 'pass'})
        self.assertJSONEqual(response.content, status_ok.content)
        self.assertTrue(response.cookies)

        response = c.post(url, {'cookies': 'true'})
        self.assertJSONEqual(response.content, status_ok.content)

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

    def test_validation(self):
        url = '/auth/login'
        c = self.client

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

    def test_auth_error(self):
        url = '/auth/login'
        c = self.client

        response = c.post(url, {'username': 'test', 'password': 'wrong_pass'})
        self.assertJSONEqual(response.content, auth_error.content)

        response = c.post(url, {'username': 'wrong_test', 'password': 'pass'})
        self.assertJSONEqual(response.content, auth_error.content)

        response = c.post(url, {'cookies': 'true'})
        self.assertJSONEqual(response.content, auth_error.content)

    def test_is_active(self):
            url = '/auth/login'
            c = self.client

            response = c.post(url, {'username': 'test', 'password': 'pass'})
            self.assertJSONEqual(response.content, status_ok.content)

            user = User.objects.filter(username='test')[0]
            user.is_active = False
            user.save()

            response = c.post(url, {'cookies': 'true'})
            self.assertJSONEqual(response.content, user_not_active.content)

            response = c.post(url, {'username': 'test', 'password': 'pass'})
            self.assertJSONEqual(response.content, user_not_active.content)
