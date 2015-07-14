from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.proceed, name='proceed'),
    url(r'^read$', views.get_post, name='get_post')
]
