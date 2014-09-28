import django.contrib.auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

def home(request):
    """
    Show the homepage.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("/ranking/overview")
    return render(request, "juggerranking/home.html")

def login(request):
    """
    Logs the user in.
    """
    if request.method != "POST":
        return HttpResponseRedirect("/")
    username = request.POST["username"]
    password = request.POST["password"]
    user = django.contrib.auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        django.contrib.auth.login(request, user)
        return HttpResponseRedirect("/ranking/overview")
    else:
        return HttpResponseRedirect("/")

def logout(request):
    """
    Logs the user out.
    """
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/")
