from juggerranking.models import Game, Team
from django.contrib import admin

class TeamAdmin(admin.ModelAdmin):
    """
    Controls how teams are shown in Django's Admin interface.
    """
    # which fields are shown?
    list_display = ("name",)
    # by which attributes can we filter?
    list_filter = ["name",]
    # in which fields can we search?
    search_fields = ["name",]

admin.site.register(Team, TeamAdmin)

class GameAdmin(admin.ModelAdmin):
    """
    Controls how games are shown in Django's Admin interface.
    """
    # which fields are shown?
    list_display = ("id", "team_1", "team_2", "score_1", "score_2")
    # by which attributes can we filter?
    list_filter = ["team_1", "team_2"]
    # in which fields can we search?
    search_fields = ["team_1", "team_2", "score_1", "score_2"]

admin.site.register(Game, GameAdmin)
