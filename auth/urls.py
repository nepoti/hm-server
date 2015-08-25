from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    # url(r'^edit$', views.edit, name='edit'),
    url(r'^restore$', views.restore, name='restore'),
    url(r'^restore/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.restore_confirm, name='password_reset_confirm'),
    url(r'^success2/$', views.success2, name='success2'),
]
