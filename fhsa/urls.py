from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
     url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    ]
