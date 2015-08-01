from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from response.templates import task_error, invalid_data
from response.templates import ok_response, error_response, status_ok
from datetime import date


allowed_keys = {'name': 30, 'profile_image': 200, 'gender': 20, 'country': 50, 'city': 200, 'about': 100}
limit = 20


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    profile_image = models.URLField(blank=True, default=u'')
    gender = models.CharField(blank=True, default=u'', max_length=20)
    country = models.CharField(blank=True, default=u'', max_length=50)
    city = models.CharField(blank=True, default=u'', max_length=200)
    birthday = models.DateField(blank=True, null=True)
    about = models.CharField(blank=True, default=u'',  max_length=100)
    achievements = models.TextField(default=u'{}')

    def get_info(self):
        if not self.user.is_active:
            return [{'id': self.id, 'name': self.name, 'username': self.user.username, 'is_active': False}]
        return [{'id': self.id, 'name': self.name, 'profile_image': self.profile_image, 'gender': self.gender,
                'country': self.country, 'city': self.city, 'birthday': self.birthday, 'about': self.about,
                 'achievements': self.achievements, 'username': self.user.username, 'is_active': True,
                 'followers': self.followers.count(), 'following': self.following.count(), 'posts': self.posts.count()}]

    def set_info(self, data):
        if type(data) is not dict:
            return task_error
        results = {}
        error = False
        for key in data:
            if key in allowed_keys and type(key) is unicode:
                if type(data[key]) is not unicode:
                    results[key] = False
                elif len(data[key]) > allowed_keys[key]:
                    results[key] = False
                else:
                    setattr(self, key, data[key])
                    results[key] = True
            elif key == 'birthday':
                results[key] = self.set_birthday(data[key])
            else:
                results[key] = False
            if not results[key]:
                error = True
        self.save()
        if error:
            return error_response(50, [results])
        return ok_response([results])

    def set_birthday(self, birthday):
        if type(birthday) is not list:
            return False
        length = len(birthday)
        if length != 3 and length != 0:
            return False
        try:
            if length == 3:
                obj = date(int(birthday[0]), int(birthday[1]), int(birthday[2]))
            else:  # length == 1
                obj = None
        except:
            return False
        self.birthday = obj
        return True

    def follow_add(self, follow_id):
        try:
            follow_id = int(follow_id)
            obj = UserProfile.objects.filter(id=follow_id)[0]
        except:
            return invalid_data
        if self == obj:
            return invalid_data
        if not Follow.objects.filter(following=obj, follower=self).exists():
            follow_obj = Follow(following=obj, follower=self)
            follow_obj.save()
        return status_ok

    def follow_remove(self, follow_id):
        try:
            follow_id = int(follow_id)
            obj = UserProfile.objects.filter(id=follow_id)[0]
        except:
            return invalid_data
        if self == obj:
            return invalid_data
        Follow.objects.filter(following=obj, follower=self).delete()
        return status_ok

    def follower_remove(self, follower_id):
        try:
            follower_id = int(follower_id)
            obj = UserProfile.objects.filter(id=follower_id)[0]
        except:
            return invalid_data
        if self == obj:
            return invalid_data
        Follow.objects.filter(following=self, follower=obj).delete()
        return status_ok

    def get_posts(self, page=0, limit=10):
        count = self.posts.count()
        response = {'limit': limit, 'page': page, 'count': count}
        start = page*limit
        end = start+limit
        if start >= count:
            response['data'] = []
            return ok_response([response])
        queryset = self.posts.all()[start:end]
        response['data'] = list([{'id': post.id, 'timestamp': post.timestamp, 'author': post.author.id,
                                  'text': post.text, 'photos': post.photos, 'locations': post.locations,
                                  'likes': post.likes.count(), 'comments': post.comments.count()}
                                 for post in queryset])
        return ok_response([response])

    def get_followers(self, page=0):
        count = self.followers.count()
        response = {'limit': limit, 'page': page, 'count': count}
        start = page*limit
        end = start+limit
        if start >= count:
            response['data'] = []
            return ok_response([response])
        queryset = [x.follower for x in self.followers.all()[start:end]]
        response['data'] = list([{'id': user.id,
                                  'name': user.name,
                                  'profile_image': user.profile_image,
                                  'username': user.user.username}
                                 for user in queryset])
        return ok_response([response])

    def get_following(self, page=0):
        count = self.following.count()
        response = {'limit': limit, 'page': page, 'count': count}
        start = page*limit
        end = start+limit
        if start >= count:
            response['data'] = []
            return ok_response([response])
        queryset = [x.following for x in self.following.all()[start:end]]
        response['data'] = list([{'id': user.id,
                                  'name': user.name,
                                  'profile_image': user.profile_image,
                                  'username': user.user.username}
                                 for user in queryset])
        return ok_response([response])


class Follow(models.Model):
    following = models.ForeignKey(UserProfile, related_name='followers')
    follower = models.ForeignKey(UserProfile, related_name='following')
