import React from 'react';
import Player from './Player';

class Game extends React.Component {
    constructor (props) {

        super(props);
        this.state = {
            userType: null,
            playing: false,
            players: []
        }

        //Add event listener to listen for websocket messages
        document.getElementById("root").addEventListener('message', this.responseHandler.bind(this));
    }

    responseHandler (e) {

        let message = e.detail.message;

        console.log(message.type);
    
        if (message.type === 'user_type_response') {
            //first message, received after a player joins the game
    
            //Reset userType only if this is the first message to be received
            let userType = this.state.userType
            if (userType === null) {
                userType = message.user_type
            }
    
            this.setState({
                userType: userType,
                players: message.players
            })
        } else {
            //Messages updating the game state
            console.log(e.detail.message);
            let newState = e.detail.message.state;
            this.setState(newState);
        }
    }

    render() {
        return (
            <div>
                <div>
                    GAME
                </div>
                <div>
                    {this.state.players.map(player => (
                        <Player player={player} />
                    ))}
                </div>
                {!this.state.playing && this.state.userType === 'host' ?
                    <button type="button" onClick={() => {
                        this.props.socket.send({
                            'type': 'start_game'
                        })
                    }}>
                        Start Game
                    </button> :
                    ""
                }
            </div>
        )
    }
}

export default Game;