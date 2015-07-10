from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from response.templates import task_error, invalid_data
from response.templates import ok_response, error_response, status_ok
from datetime import date


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
    allowed_keys = {'name': 30, 'profile_image': 200, 'gender': 20, 'country': 50, 'city': 200, 'about': 100}

    def get_info(self):
        return [{'id': self.id, 'name': self.name, 'profile_image': self.profile_image, 'gender': self.gender,
                'country': self.country, 'city': self.city, 'birthday': self.birthday, 'about': self.about,
                 'achievements': self.achievements,
                 'followers': len(self.followers), 'following': len(self.following)}]

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

    def get_posts(self):
        return list([post.id for post in self.posts.order_by('-timestamp')])

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

    def get_followers(self):
        return ok_response(str(self.followers.all())+str(self.following.all()))
