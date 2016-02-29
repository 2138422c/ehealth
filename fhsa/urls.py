from django.conf.urls import patterns, url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
     url(r'^register/$', views.register, name='register'),
    url(r'^login/$',login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^about/$', views.about, name="about"),
    url(r'^user_page/$', views.user_page, name="user_page"),
    ]