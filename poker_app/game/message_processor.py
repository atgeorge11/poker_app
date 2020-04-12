#Processes messages from client websockets

def process_message (message, game_state, username, user_type):

    #Process user type requests
    if message['type'] == "user_type_request":
        return {
            'type': 'user_type_response',
            'user_type': user_type,
            'id': len(game_state.players) - 1,
            'players': game_state.players
        }

    #Process start game requests
    elif message['type'] == "start_game":
        #Start the game
        game_state.start_game()
        return {
            'type': 'play',
            'state': {
                'playing': True,
                'dealer': game_state.dealer
            }
        }

    #Process other requests
