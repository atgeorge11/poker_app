from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .poker_logic.game_states import game_states
from .poker_logic.game_state import Game_State

@login_required
def create (request):
    """create a game"""
    game_name = request.POST.dict()['game_name_create']
    game_states[game_name] = Game_State()
    return redirect('game:gameroom', game_name=game_name)

@login_required
def join (request):
    """join a game"""
    game_name = request.POST.dict()['game_name_join']
    if game_name in game_states and game_states[game_name].playing == False:
        return redirect('game:gameroom', game_name=game_name)
    else:
        return redirect('main:index')

@login_required
def gameroom (request, game_name):
    return render(request, 'build/index.html', {'game_name':game_name})
