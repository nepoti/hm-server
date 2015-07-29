from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile


class UserProfileCreate(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register', {'username': 'test', 'password': 'pass',
                                                       'email': 'admin@gmail.com'})
        self.assertJSONEqual(response.content, status_ok.content)

    def test_profile_create(self):
        profile = UserProfile.objects.filter(user__username='test')
        self.assertTrue(profile.exists())

        profile = profile[0]
        self.assertEqual(profile.name, 'test')
        self.assertEqual(profile.achievements, '{}')