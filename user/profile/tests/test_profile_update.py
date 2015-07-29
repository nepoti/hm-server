from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile
from json import loads, dumps
from datetime import date


class UserProfileUpdate(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register',
                                    {'username': 'test', 'password': 'pass', 'email': 'admin@gmail.com'})
        self.assertEqual(response.content, status_ok.content)
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertTrue(response.cookies)

    def test_validation(self):
        url = '/user/profile/update'
        c = Client()

        response = c.post(url, {})
        self.assertEqual(response.content, auth_error.content)

        response = c.post(url, {'data': {}})
        self.assertEqual(response.content, auth_error.content)

        c = self.client

        response = c.post(url, {})
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'data': {'wrong_data'}})
        self.assertEqual(response.content, invalid_data.content)

        response = c.post(url, {'data':
                                dumps(
                                    {'name': 'q'*31, 'profile_image': 'q'*201, 'gender': 'q'*21,
                                     'country': 'q'*51, 'city': 'q'*201, 'about': 'q'*101,
                                     'birthday': [0, 0, 0]
                                     }
                                )
                                }
                          )
        content = loads(response.content)
        self.assertEqual(content['status'], 0)
        self.assertEqual(content['error'], 50)
        data = content['result'][0]
        self.assertTrue(True not in data.values())

    def test_profile_update(self):
        url = '/user/profile/update'
        c = self.client

        response = c.post(url, {'data':
                                dumps(
                                    {'name': 'q'*30, 'profile_image': 'q'*200, 'gender': 'q'*20,
                                     'country': 'q'*50, 'city': 'q'*200, 'about': 'q'*100,
                                     'birthday': [2000, 1, 1]
                                     }
                                )
                                }
                          )
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        data = content['result'][0]
        self.assertTrue(False not in data.values())

        profile = UserProfile.objects.filter(user__username='test')
        self.assertTrue(profile.exists())

        profile = profile[0]
        self.assertEqual(profile.name, 'q'*30)
        self.assertEqual(profile.profile_image, 'q'*200)
        self.assertEqual(profile.gender, 'q'*20)
        self.assertEqual(profile.country, 'q'*50)
        self.assertEqual(profile.city, 'q'*200)
        self.assertEqual(profile.about, 'q'*100)
        self.assertEqual(profile.birthday, date(2000, 1, 1))

        response = c.post(url, {'data': dumps({'birthday': []})})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        data = content['result'][0]
        self.assertTrue(False not in data.values())

        profile = UserProfile.objects.filter(user__username='test')
        self.assertTrue(profile.exists())

        profile = profile[0]
        self.assertEqual(profile.birthday, None)
