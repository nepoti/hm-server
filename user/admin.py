from django.contrib import admin
from user.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'country', 'city', 'birthday')
