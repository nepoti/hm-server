from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from response.templates import task_error, invalid_data
from response.templates import ok_response, error_response
from datetime import date
import constants as c


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30, default=u'')
    gender = models.CharField(blank=True, default=u'', max_length=20)
    country = models.CharField(blank=True, default=u'', max_length=50)
    city = models.CharField(blank=True, default=u'', max_length=200)
    birthday = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, default=0)
    weight = models.FloatField(blank=True, default=0)
    blood = models.IntegerField(blank=True, default=0)

    def __iter__(self):
        return [self.user, self.name]

    def __unicode__(self):
        return self.name

    def get_info(self):
        if not self.user.is_active:
            return invalid_data
        return ok_response([{'name': self.name, 'gender': self.gender, 'birthday': self.birthday,
                             'country': self.country, 'city': self.city,
                             'height': self.height, 'weight': self.weight, 'blood': self.blood
                             }])

    def set_info(self, data):
        if type(data) is not dict:
            return task_error
        results = {}
        error = False
        for key in data:
            if key in c.UserProfile_ALLOWED_KEYS and type(key) is unicode:
                if type(data[key]) is not unicode:
                    results[key] = False
                elif len(data[key]) > c.UserProfile_ALLOWED_KEYS[key]:
                    results[key] = False
                else:
                    setattr(self, key, data[key])
                    results[key] = True
            elif key == 'birthday':
                results[key] = self.set_birthday(data[key])
            elif key == 'height' or key == 'weight':
                try:
                    t = float(data[key])
                    setattr(self, key, t)
                    results[key] = True
                except:
                    results[key] = False
            elif key == 'blood':
                try:
                    t = int(data[key])
                    if t not in c.UserProfile_BLOOD_CHOICES:
                        results[key] = False
                    else:
                        setattr(self, key, t)
                        results[key] = True
                except:
                    results[key] = False
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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)