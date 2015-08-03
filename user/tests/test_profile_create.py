from django.test import TestCase, Client
from response.templates import status_ok
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