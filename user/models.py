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
    followers = ArrayField(models.IntegerField())
    following = ArrayField(models.IntegerField())

    def get_info(self):
        if not self.user.is_active:
            return [{'id': self.id, 'name': self.name, 'username': self.user.username, 'is_active': False}]
        return [{'id': self.id, 'name': self.name, 'profile_image': self.profile_image, 'gender': self.gender,
                'country': self.country, 'city': self.city, 'birthday': self.birthday, 'about': self.about,
                 'achievements': self.achievements, 'username': self.user.username, 'is_active': True,
                 'followers': len(self.followers), 'following': len(self.following), 'posts': self.posts.count()}]

    def set_info(self, data):
        if type(data) is not dict:
            return task_error
        results = {}
        error = False
        for key in data:
            if key in self.allowed_keys and type(key) is unicode:
                if type(data[key]) is not unicode:
                    results[key] = False
                elif len(data[key]) > self.allowed_keys[key]:
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
            return error_response(50, results)
        return ok_response([results])

    def set_birthday(self, birthday):
        if len(birthday) != 3:
            return False
        try:
            obj = date(int(birthday[0]), int(birthday[1]), int(birthday[2]))
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
        if follow_id not in self.following:
            self.following.append(follow_id)
            self.save()
        if self.id not in obj.followers:
            obj.followers.append(self.id)
            obj.save()
        return status_ok

    def follow_remove(self, follow_id):
        try:
            follow_id = int(follow_id)
            obj = UserProfile.objects.filter(id=follow_id)[0]
        except:
            return invalid_data
        if self == obj:
            return invalid_data
        if follow_id in self.following:
            self.following.remove(follow_id)
            self.save()
        if self.id in obj.followers:
            obj.followers.remove(self.id)
            obj.save()
        return status_ok

    def follower_remove(self, follower_id):
        try:
            follower_id = int(follower_id)
            obj = UserProfile.objects.filter(id=follower_id)[0]
        except:
            return invalid_data
        if self == obj:
            return invalid_data
        if follower_id in self.followers:
            self.followers.remove(follower_id)
            self.save()
        if self.id in obj.following:
            obj.following.remove(self.id)
            obj.save()
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
        count = len(self.followers)
        response = {'limit': limit, 'page': page, 'count': count}
        start = page*limit
        end = start+limit
        if start >= count:
            response['data'] = []
            return ok_response([response])
        to_search = self.followers[start:end]
        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(to_search)])
        ordering = 'CASE %s END' % clauses
        queryset = UserProfile.objects.filter(id__in=to_search)\
            .extra(select={'ordering': ordering}, order_by=('ordering',))
        response['data'] = list([{'id': user.id,
                                  'name': user.name,
                                  'profile_image': user.profile_image,
                                  'username': user.user.username}
                                 for user in queryset])
        return ok_response([response])

    def get_following(self, page=0):
        count = len(self.following)
        response = {'limit': limit, 'page': page, 'count': count}
        start = page*limit
        end = start+limit
        if start >= count:
            response['data'] = []
            return ok_response([response])
        to_search = self.following[start:end]
        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(to_search)])
        ordering = 'CASE %s END' % clauses
        queryset = UserProfile.objects.filter(id__in=to_search)\
            .extra(select={'ordering': ordering}, order_by=('ordering',))
        response['data'] = list([{'id': user.id,
                                  'name': user.name,
                                  'profile_image': user.profile_image,
                                  'username': user.user.username}
                                 for user in queryset])
        return ok_response([response])
