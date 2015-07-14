from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.proceed_post, name='proceed'),
    url(r'^read$', views.get_post, name='get_post'),
    url(r'^comment$', views.proceed_comment, name='comment'),
    url(r'^comment/read$', views.get_comment, name='get_comment'),
]
