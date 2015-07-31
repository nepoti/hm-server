from django.test import TestCase, Client
from response.templates import username_not_valid, username_already_exist
from response.templates import email_not_valid, email_already_exist
from response.templates import auth_error, user_not_active, task_error, invalid_data, status_ok
from django.contrib.auth.models import User
from social.models import UserProfile
from json import loads


class UserFollow(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.post('/auth/register', {'username': 'test', 'password': 'pass',
                                                       'email': 'admin@gmail.com'})
        response = self.client.post('/auth/register', {'username': 'test2', 'password': 'pass2',
                                                       'email': 'admin2@gmail.com'})
        self.assertJSONEqual(response.content, status_ok.content)
        # login 1st user
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertEqual(response.content, status_ok.content)

    def test_user_follow(self):
        follow_url = '/user/follow'
        following_url = '/user/following'
        followers_url = '/user/followers'
        c = self.client

        profile = UserProfile.objects.filter(user__username='test')[0]
        profile2 = UserProfile.objects.filter(user__username='test2')[0]

        # check that 1st user have 0 following
        response = c.post(following_url, {})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

        # check that results don't change when id and page is passed
        response2 = c.post(following_url, {'id': profile.id, 'page': 0})
        self.assertEqual(response.content, response2.content)

        # check that 1st user have 0 followers
        response = c.post(followers_url, {})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

        # check that results don't change when id and page is passed
        response2 = c.post(followers_url, {'id': profile.id, 'page': 0})
        self.assertEqual(response.content, response2.content)

        # 1st user become a follower of 2nd user
        response = c.post(follow_url, {'id': profile2.id})
        self.assertEqual(response.content, status_ok.content)

        # check that 1st user is a follower of 2nd user
        response = c.post(following_url)
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 1)
        self.assertEqual(result['page'], 0)
        data = result['data']
        self.assertEqual(len(data), 1)
        data = data[0]
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['profile_image'], '')
        self.assertEqual(data['username'], 'test2')
        self.assertEqual(data['id'], profile2.id)

        response2 = c.post(following_url, {'id': profile.id, 'page': 0})
        self.assertEqual(response.content, response2.content)

        response = c.post(followers_url, {'id': profile2.id})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 1)
        self.assertEqual(result['page'], 0)
        data = result['data']
        self.assertEqual(len(data), 1)
        data = data[0]
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['profile_image'], '')
        self.assertEqual(data['username'], 'test')
        self.assertEqual(data['id'], profile.id)

        response2 = c.post(followers_url, {'id': profile2.id, 'page': 0})
        self.assertEqual(response.content, response2.content)

        # 1st user cancel following 2nd user
        response = c.delete(follow_url, 'id='+str(profile2.id))
        self.assertEqual(response.content, status_ok.content)

        # check that 1st user have 0 following
        response = c.post(following_url, {})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

        # check that 2nd user have 0 followers
        response = c.post(followers_url, {'id': profile2.id})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

        # login 2nd user
        response = c.post('/auth/login', {'username': 'test2', 'password': 'pass2'})
        self.assertEqual(response.content, status_ok.content)

        # 2nd user become a follower of 1st user
        response = c.post(follow_url, {'id': profile.id})
        self.assertEqual(response.content, status_ok.content)

        # login 1st user
        response = c.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertEqual(response.content, status_ok.content)

        # 1st user remove 2nd user from followers
        response = c.delete(followers_url, 'id=' + str(profile2.id))
        self.assertEqual(response.content, status_ok.content)

        # check that 1st user have 0 followers
        response = c.post(followers_url, {'id': profile.id})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

        # check that 2nd user have 0 following
        response = c.post(following_url, {'id': profile2.id})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)
        result = content['result'][0]
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['data'], [])

    def test_validation(self):
        follow_url = '/user/follow'
        following_url = '/user/following'
        followers_url = '/user/followers'
        c = self.client

        profile = UserProfile.objects.filter(user__username='test')[0]
        profile2 = UserProfile.objects.filter(user__username='test2')[0]

        wrong_id = max(profile.id, profile2.id) + 1
        wrong_page = -1

        # follow_url without params
        response = c.post(follow_url, {})
        self.assertEqual(response.status_code, 404)
        response = c.delete(follow_url, '')
        self.assertEqual(response.status_code, 404)

        # follow_url with wrong id
        response = c.post(follow_url, {'id': wrong_id})
        self.assertEqual(response.content, invalid_data.content)
        response = c.delete(follow_url, 'id=' + str(wrong_id))
        self.assertEqual(response.content, invalid_data.content)

        # followers_url with wrong id
        response = c.post(followers_url, {'id': wrong_id})
        self.assertEqual(response.content, invalid_data.content)
        response = c.delete(followers_url, 'id=' + str(wrong_id))
        self.assertEqual(response.content, invalid_data.content)

        # following_url with wrong id
        response = c.post(following_url, {'id': wrong_id})
        self.assertEqual(response.content, invalid_data.content)

        # followers_url with wrong page
        response = c.post(followers_url, {'page': wrong_page})
        self.assertEqual(response.content, invalid_data.content)

        # following_url with wrong page
        response = c.post(following_url, {'page': wrong_page})
        self.assertEqual(response.content, invalid_data.content)
