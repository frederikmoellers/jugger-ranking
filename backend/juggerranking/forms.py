from django.core.exceptions import ValidationError
from django.forms import ModelForm
from models import Game, Team

class GameForm(ModelForm):
    class Meta:
        model = Game

    def __init__(self, user, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields["team_1"].queryset = Team.objects.filter(user = user)
        self.fields["team_2"].queryset = Team.objects.filter(user = user)

    def clean(self):
        self.cleaned_data = super(GameForm, self).clean()
        if "team_1" in self.cleaned_data and "team_2" in self.cleaned_data:
            if self.cleaned_data["team_1"] == self.cleaned_data["team_2"]:
                raise ValidationError("Games must be between different teams!")
        if "score_1" in self.cleaned_data and "score_2" in self.cleaned_data:
            if self.cleaned_data["score_1"] == self.cleaned_data["score_2"]:
                raise ValidationError("Games cannot result in a tie!")
        return self.cleaned_data
