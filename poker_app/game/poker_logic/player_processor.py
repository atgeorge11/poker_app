"""Processes players for data transmission to client"""

class Player_Processor():
    @classmethod
    def process_players (cls, players, hands, include_cards):
        output = []
        for player in players:
            if player is not None:
                hand = []
                if include_cards == True:
                    hand = hands[str(player.id)]
                elif str(player.id) in hands and len(hands[str(player.id)]) > 0:
                    hand = ['xx', 'xx']
                output.append({
                    'player': player.username,
                    'id': player.id,
                    'chips': player.chips,
                    'user_type': player.user_type,
                    'next': player.get_next().id,
                    'prev': player.get_prev().id,
                    'status': player.status,
                    'hand': hand,
                    'bet': player.bet
                })
        return output