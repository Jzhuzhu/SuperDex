from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('pokemon.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^pokemon/', include('pokemon.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$','django.views.static.serve',
    	{'document_root':settings.STATIC_ROOT}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
