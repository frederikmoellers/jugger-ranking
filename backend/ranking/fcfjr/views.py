from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logic
from juggerranking.models import Game, Team
from ranking.models import RankedTeam

@login_required
def recalculate(request):
    logic.recalculate(request.user)
    return HttpResponseRedirect("/ranking/overview")
