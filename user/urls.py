from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^profile/', include('user.profile.urls')),
    url(r'^remove$', views.remove, name='remove'),
]
