from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Default site is home
    url(r'^$', 'juggerranking.views.home'),

    url(r'^login/?$', 'juggerranking.views.login'),
    url(r'^logout/?$', 'juggerranking.views.logout'),

    url(r'^ranking/', include('ranking.urls')),
)

from django.conf import settings
## debug stuff to serve static media
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
   )
