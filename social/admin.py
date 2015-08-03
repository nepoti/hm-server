from django.contrib import admin
from social.models import Post, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'timestamp', 'text', 'photos', 'locations')


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'timestamp', 'text', 'photos', 'locations')
