from django.test import TestCase, Client
from django.contrib.auth.models import User
from json import loads
from urlparse import urlparse
from social.models import UploadUrl


class UserImgupload(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='test', password='pass')
        response = self.client.post('/auth/login', {'username': 'test', 'password': 'pass'})
        self.assertTrue(response.cookies)

    def test_validation(self):
        url = '/user/imgupload'
        c = self.client

        response = c.post(url)
        self.assertEqual(response.status_code, 404)

        response = c.post(url, {'length': 0})
        content = loads(response.content)
        self.assertEqual(content['status'], 0)
        self.assertEqual(content['error'], 51)

        response = c.post(url, {'length': -1})
        content = loads(response.content)
        self.assertEqual(content['status'], 0)
        self.assertEqual(content['error'], 51)

    def test_imgupload(self):
        url = '/user/imgupload'
        c = self.client

        response = c.post(url, {'length': 1024})
        content = loads(response.content)
        self.assertEqual(content['status'], 1)
        self.assertEqual(content['error'], 0)

        img = urlparse(content['result'][0])

        self.assertEqual(img.hostname, 'thehealthme.s3.eu-central-1.amazonaws.com')
        self.assertEqual(len(img.path), 69)
        self.assertTrue(img.path.endswith('.jpg'))
        self.assertEqual(img.scheme, 'https')

        query = img.query
        self.assertTrue(False not in [x in query for x in
                                      ('X-Amz-Algorithm=AWS4-HMAC-SHA256',
                                       'X-Amz-Expires=3600',
                                       'X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost',
                                       'X-Amz-Signature',
                                       'X-Amz-Date',
                                       'X-Amz-Credential')])

        self.assertEqual(UploadUrl.objects.all()[0].key, img.path[1:65])
