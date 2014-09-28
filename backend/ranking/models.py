from django.contrib.auth.models import User
from django.db import models
from juggerranking.models import Team

class RankedTeam(models.Model):
    place = models.PositiveIntegerField(editable = False, help_text = "Team's rank")
    team = models.ForeignKey(Team, help_text = "Team", related_name = "ranking")

class UserRankingProperties(models.Model):
    user = models.ForeignKey(User, primary_key = True, related_name = "ranking_preferences")
    method = models.CharField(max_length = 100, help_text = "Ranking Method")
    hot = models.BooleanField(default = False, editable = False, help_text = "Ranking cache valid?")
