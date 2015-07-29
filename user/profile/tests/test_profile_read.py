from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile
from json import loads


class UserProfileRead(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register',
                                    {'username': 'test', 'password': 'pass', 'email': 'admin@gmail.com'})
        self.assertEqual(response.content, status_ok.content)
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertTrue(response.cookies)

    def test_validation(self):
        url = '/user/profile/read'
        c = Client()

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'id': 1})
        self.assertEqual(response.status_code, 404)

        c = self.client

        response = c.post(url, {'id': 'a'})
        self.assertEqual(response.content, invalid_data.content)

    def test_current_user(self):
        url = '/user/profile/read'
        c = self.client

        response = c.post(url)

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)

        data = content['result'][0]
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['profile_image'], '')
        self.assertEqual(data['gender'], '')
        self.assertEqual(data['country'], '')
        self.assertEqual(data['city'], '')
        self.assertEqual(data['birthday'], None)
        self.assertEqual(data['about'], '')
        self.assertEqual(data['achievements'], '{}')
        self.assertEqual(data['followers'], 0)
        self.assertEqual(data['following'], 0)
        self.assertEqual(data['posts'], 0)
        self.assertEqual(data['is_active'], True)

    def test_other_user(self):
        url = '/user/profile/read'
        c = self.client

        response = c.post('/auth/register', {'username': 'test2', 'password': 'pass2', 'email': 'admin2@gmail.com'})
        self.assertEqual(response.content, status_ok.content)

        profile = UserProfile.objects.filter(user__username='test2')[0]

        response = c.post(url, {'id': profile.id})

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)

        data = content['result'][0]
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['profile_image'], '')
        self.assertEqual(data['gender'], '')
        self.assertEqual(data['country'], '')
        self.assertEqual(data['city'], '')
        self.assertEqual(data['birthday'], None)
        self.assertEqual(data['about'], '')
        self.assertEqual(data['achievements'], '{}')
        self.assertEqual(data['followers'], 0)
        self.assertEqual(data['following'], 0)
        self.assertEqual(data['posts'], 0)
        self.assertEqual(data['is_active'], True)
