from django.contrib import admin
from user.models import UserProfile, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'country', 'city', 'birthday', 'about')


@admin.register(Follow)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('following', 'follower')
