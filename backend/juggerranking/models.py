from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

class Team(models.Model):
    class Meta:
        unique_together = (("name", "user"),)

    hidden_from_ranking = models.BooleanField(default = False, help_text = "Hide this team in the ranking.")
    name = models.CharField(help_text = "The name of the team.", max_length = 100)
    user = models.ForeignKey(User, editable = False, help_text = "User", related_name = "teams")

    def __unicode__(self):
        return self.name

    def games(self):
        return Game.objects.filter(Q(team_1 = self) | Q(team_2 = self))

    def normalized_jugg_diff(self, opponents = None):
        if opponents is None:
            games = Game.objects.filter(Q(team_1 = self) | Q(team_2 = self))
        else:
            games = Game.objects.filter(Q(team_1 = self, team_2__in = opponents) | Q(team_2 = self, team_1__in = opponents))
        jd = 0.0
        if games.count() == 0:
            return jd
        for game in games:
            jd += game.jugg_diff(self)
        return jd / games.count()

class Game(models.Model):
    team_1 = models.ForeignKey(Team, help_text = "Team 1", related_name = "games_1")
    team_2 = models.ForeignKey(Team, help_text = "Team 2", related_name = "games_2")
    score_1 = models.PositiveSmallIntegerField(help_text = "Score Team 1")
    score_2 = models.PositiveSmallIntegerField(help_text = "Score Team 2")

    def __unicode__(self):
        return "%s:%s - %d:%d" % (self.team_1, self.team_2, self.score_1, self.score_2)

    def jugg_diff(self, team = None):
        if team == self.team_1:
            return self.score_1 - self.score_2
        elif team == self.team_2:
            return self.score_2 - self.score_1
        return abs(self.score_1 - self.score_2)

    def loser(self):
        if self.score_1 < self.score_2:
            return self.team_1
        return self.team_2
    
    def winner(self):
        if self.score_1 > self.score_2:
            return self.team_1
        return self.team_2
