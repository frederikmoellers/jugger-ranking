from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^overview$', 'ranking.views.ranking', name='ranking'),
    url(r'^newteam$', 'ranking.views.new_team', name='new_team'),
    url(r'^removeteam$', 'ranking.views.remove_team', name='remove_team'),
    url(r'^newgame$', 'ranking.views.new_game', name='new_game'),
    url(r'^removegame$', 'ranking.views.remove_game', name='remove_game'),
    url(r'fcfjr/', include('ranking.fcfjr.urls')),
)
