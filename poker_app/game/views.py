from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def create (request):
    """create a game"""
    game_name = request.POST.dict()['game_name_create']
    return redirect('game:gameroom', game_name=game_name)

@login_required
def join (request):
    """join a game"""
    game_name = request.POST.dict()['game_name_join']
    return redirect('game:gameroom', game_name=game_name)

@login_required
def gameroom (request, game_name):
    return render(request, 'build/index.html', {'game_name':game_name})
