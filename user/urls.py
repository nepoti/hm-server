from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^remove$', views.remove, name='remove'),
    url(r'^posts$', views.get_posts, name='get_posts'),
    url(r'^profile/', include('user.profile.urls')),
]
