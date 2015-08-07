from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.proceed_post, name='proceed'),
    url(r'^read$', views.get_post, name='get_post'),
    url(r'^like$', views.like_post, name='like_post'),
    url(r'^likes$', views.get_likes, name='get_likes'),
    url(r'^comments$', views.get_comments, name='get_comments'),
    url(r'^comment$', views.proceed_comment, name='comment'),
    url(r'^comment/read$', views.get_comment, name='get_comment'),
    url(r'^comment/like$', views.like_comment, name='like_comment'),
    url(r'^comment/likes$', views.get_comment_likes, name='get_comment_likes'),
]
