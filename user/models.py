from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from response.templates import task_error
from response.templates import ok_response, error_response
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
        return {'id': self.id, 'name': self.name, 'profile_image': self.profile_image, 'gender': self.gender,
                'country': self.country, 'city': self.city, 'birthday': self.birthday, 'about': self.about,
                'achievements': self.achievements, 'followers': self.followers, 'following': self.following}

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
            elif key == 'followers':
                results[key] = self.remove_follower(data[key])
            elif key == 'following':
                results[key] = self.change_following(data[key])
            else:
                results[key] = False
            if not results[key]:
                error = True
        self.save()
        if error:
            return error_response(50, results)
        return ok_response(results)

    def set_birthday(self, birthday):
        if len(birthday) != 3:
            return False
        try:
            obj = date(int(birthday[0]), int(birthday[1]), int(birthday[2]))
        except:
            return False
        self.birthday = obj
        return True

    def change_following(self, data):
        if len(data) != 2:
            return False
        if data[0] != '+' and data[0] != '-':
            return False
        try:
            following_id = int(data[1])
            obj = UserProfile.objects.filter(id=following_id)[0]
        except:
            return False
        if self == obj:
            return False
        if data[0] == '-':
            if following_id in self.following:
                self.following.remove(following_id)
            if self.id in obj.followers:
                obj.followers.remove(self.id)
                obj.save()
        else:  # '+'
            if following_id in self.following:
                return True
            if self.id not in obj.followers:
                obj.followers.append(self.id)
                obj.save()
            self.following.append(following_id)
        return True

    def remove_follower(self, data):
        try:
            follower_id = int(data)
            obj = UserProfile.objects.filter(id=follower_id)[0]
        except:
            return False
        if self == obj:
            return False
        if follower_id in self.followers:
            self.followers.remove(follower_id)
        if self.id in obj.following:
            obj.following.remove(self.id)
            obj.save()
        return True
