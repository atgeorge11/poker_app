"""Class that holds general information about the game"""

class Game_State():
    def __init__(self):

        #data about players
        self.players = []
        
        #controls whether game has started or whether more players can joing
        self.playing = False

    """generate a new player"""
    def generate_player(self, username, starting_chips, user_type):
        print("username", username)
        print("starting_chips", starting_chips)
        print("user_type", user_type)
        new_player =  {
            'player': username,
            'starting_chips': starting_chips,
            'user_type': user_type
        }
        self.players.append(new_player)

    """remove a player from the game"""
    def remove_player(self, username):
        for player in self.players:
            if player['player'] == username:
                self.players.remove(player) 
                break




