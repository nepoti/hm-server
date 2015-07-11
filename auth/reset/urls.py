from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.reset, name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        views.reset_confirm, name='password_reset_confirm'),
    url(r'^success/$', views.success, name='success'),
    url(r'^success2/$', views.success2, name='success2'),
]
