from django.conf.urls import include,url

from . import views

urlpatterns = [
    url(r'^read$', views.read, name='read'),
    url(r'^update$', views.update, name='update'),
]
