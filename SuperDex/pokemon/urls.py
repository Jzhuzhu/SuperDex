from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<pokemon_id>\d+)/$', views.pokemon_profile, name='Profile'),
	url(r'^search/$', views.search, name="Search"),
	url(r'^comparison/$', views.index_comparison, name="Comparison"),
	url(r'^comp_search/$', views.comp_search, name="Comparison"),
)