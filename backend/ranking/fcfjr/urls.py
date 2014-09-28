from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'recalculate/$', 'ranking.fcfjr.views.recalculate', name='fcfjr-recalculate'),
)
