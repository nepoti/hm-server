from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^status$', views.is_logged_in, name='is_logged_in'),
    url(r'^email$', views.email_change, name='email_change'),
    url(r'^password$', views.pass_change, name='pass_change'),
    url(r'^reset/', include('auth.reset.urls')),
]
