from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from juggerranking.forms import GameForm
from juggerranking.models import Game, Team
from models import RankedTeam, RankingPicture

@login_required
def new_game(request):
    if request.method != "POST":
        return HttpResponseRedirect("overview")
    form = GameForm(request.user, request.POST)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect("overview")

@login_required
def new_team(request):
    if request.method != "POST" or "name" not in request.POST:
        return HttpResponseRedirect("overview")
    try:
        Team.objects.create(name = request.POST["name"], user = request.user)
    except:
        pass
    return HttpResponseRedirect("overview")

@login_required
def overview(request):
    ranked_teams = RankedTeam.objects.filter(team__user = request.user).order_by('place')
    games = Game.objects.filter(team_1__user = request.user, team_2__user = request.user).order_by('-id')
    unranked_teams = request.user.teams.order_by('name').filter(ranking = None)
    ranking_pictures = RankingPicture.objects.filter(user = request.user)
    return render(request, "ranking/overview.html", {"game_form" : GameForm(request.user), "games" : games, "pictures" : ranking_pictures, "ranked_teams" : ranked_teams, "unranked_teams" : unranked_teams})

@login_required
def remove_game(request):
    if request.method != "GET" or "id" not in request.GET:
        return HttpResponseRedirect("overview")
    try:
        Game.objects.get(id = request.GET["id"], team_1__user = request.user, team_2__user = request.user).delete()
    except:
        pass
    return HttpResponseRedirect("overview")

@login_required
def remove_team(request):
    if request.method != "GET" or "id" not in request.GET:
        return HttpResponseRedirect("overview")
    try:
        Team.objects.get(id = request.GET["id"], user = request.user).delete()
    except:
        pass
    return HttpResponseRedirect("overview")
