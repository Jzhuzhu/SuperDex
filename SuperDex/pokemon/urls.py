from django.conf.urls import patterns, url

from pokemon import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<pokemon_id>\d+)/$', views.pokemon_profile, name='Profile'),
	url(r'^search/$', views.search, name="Search"),
)