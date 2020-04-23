"""Processes players for data transmission to client"""

class Player_Processor():
    @classmethod
    def process_players (cls, players):
        output = []
        for player in players:
            if player is not None:
                output.append({
                    'player': player.username,
                    'id': player.id,
                    'chips': player.chips,
                    'user_type': player.user_type,
                    'next': player.get_next().id,
                    'prev': player.get_prev().id,
                    'status': player.status,
                    'bet': player.bet
                })
        return output