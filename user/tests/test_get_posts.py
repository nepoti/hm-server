from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile, Post
from json import loads


class UserGetPosts(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register',
                                    {'username': 'test', 'password': 'pass', 'email': 'admin@gmail.com'})
        self.assertEqual(response.content, status_ok.content)
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertTrue(response.cookies)

    def test_validation(self):
        url = '/user/posts'
        c = self.client

        response = c.post(url, {'id': -1})
        self.assertEqual(response.content, invalid_data.content)

        response = c.post(url, {'page': -1})
        self.assertEqual(response.content, invalid_data.content)

        response = c.post(url, {'limit': -1})
        self.assertEqual(response.content, invalid_data.content)

    def test_current_user(self):
        url = '/user/posts'
        c = self.client

        profile = UserProfile.objects.filter(user__username='test')[0]

        Post(author=profile, text='post', photos=[], locations=[]).save()
        Post(author=profile, text='post2', photos=[], locations=[]).save()

        response = c.post(url, {})

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        self.assertEqual(content['result'][0]['count'], 2)
        self.assertEqual(len(content['result'][0]['data']), 2)
        self.assertEqual(content['result'][0]['data'][0]['text'], 'post2')

        response = c.post(url, {'page': 1, 'limit': 1})

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        self.assertEqual(content['result'][0]['count'], 2)
        self.assertEqual(len(content['result'][0]['data']), 1)
        self.assertEqual(content['result'][0]['data'][0]['text'], 'post')

    def test_other_user(self):
        url = '/user/posts'
        c = self.client

        response = c.post('/auth/register', {'username': 'test2', 'password': 'pass2', 'email': 'admin2@gmail.com'})
        self.assertEqual(response.content, status_ok.content)

        profile = UserProfile.objects.filter(user__username='test2')[0]

        Post(author=profile, text='post', photos=[], locations=[]).save()
        Post(author=profile, text='post2', photos=[], locations=[]).save()

        response = c.post(url, {'id': profile.id})

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        self.assertEqual(content['result'][0]['count'], 2)
        self.assertEqual(len(content['result'][0]['data']), 2)
        self.assertEqual(content['result'][0]['data'][0]['text'], 'post2')

        response = c.post(url, {'id': profile.id, 'page': 1, 'limit': 1})

        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        self.assertEqual(content['result'][0]['count'], 2)
        self.assertEqual(len(content['result'][0]['data']), 1)
        self.assertEqual(content['result'][0]['data'][0]['text'], 'post')