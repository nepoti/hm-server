from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile


class UserRemove(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register', {'username': 'test', 'password': 'pass',
                                                       'email': 'admin@gmail.com'})
        self.assertJSONEqual(response.content, status_ok.content)

    def test_user_remove(self):
        url = '/user/remove'
        c = self.client

        response = c.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertEqual(response.content, status_ok.content)

        response = c.post('/user/remove', {'password': 'pass'})
        self.assertEqual(response.content, status_ok.content)

        user = User.objects.filter(username='test')
        self.assertTrue(user.exists())

        user = user[0]
        self.assertFalse(user.is_active)

        profile = UserProfile.objects.filter(user__username='test')
        self.assertTrue(profile.exists())

        profile = profile[0]
        self.assertEqual(profile.profile_image, '')
        self.assertEqual(profile.gender, '')
        self.assertEqual(profile.country, '')
        self.assertEqual(profile.city, '')
        self.assertEqual(profile.birthday, None)
        self.assertEqual(profile.about, '')
        self.assertEqual(profile.achievements, '{}')

    def test_validation(self):
        url = '/user/remove'
        c = self.client

        # test without auth

        response = c.post(url, {})
        self.assertEqual(response.content, auth_error.content)

        response = c.post(url, {'password': 'pass'})
        self.assertEqual(response.content, auth_error.content)

        # test with auth

        response = c.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertEqual(response.content, status_ok.content)

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'password': 'wrong_pass'})
        self.assertEqual(response.content, auth_error.content)