from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^profile/', include('user.profile.urls')),
    url(r'^remove$', views.remove, name='remove'),
    url(r'^posts$', views.get_posts, name='get_posts'),
    url(r'^follow$', views.follow, name='follow'),
    url(r'^followers$', views.followers, name='followers'),
    url(r'^following$', views.following, name='following'),
    url(r'^imgupload$', views.imgupload, name='imgupload'),
]
