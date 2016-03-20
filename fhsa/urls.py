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
    url(r'^search/medline/$', views.medline, name="medline"),
    url(r'^search/$', views.search, name="search"),
    url(r'^folder/(?P<folder_name_slug>[\w\-]+)/$', views.folder, name='category'),
    url(r'^save/$', views.save, name='save'),
    url(r'^create_folder/$', views.create_folder, name="create_folder"),
    ]
