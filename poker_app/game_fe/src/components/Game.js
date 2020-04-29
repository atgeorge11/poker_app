import React from 'react';
import Player from './Player';
import Table from './Table';
import Me from './Me';
import Winner from './Winner';

import '../css/Game.css';

class Game extends React.Component {
    constructor (props) {

        super(props);
        this.state = {
            userType: null,
            username: null,
            id: null,
            playing: false,
            listening: false,
            players: [],
            startingChips: 0,
            currentPlayer: null,
            playersWithCards: [],
            table: [],
            pot: 0,
            currentBet: 0,
            blind: 10
        }

        //Add event listener to listen for websocket messages
        document.getElementById("root").addEventListener('message', this.responseHandler.bind(this));
    }

    responseHandler (e) {

        let message = e.detail.message;
    
        if (message.type === 'user_type_response') {
            //first message, received after a player joins the game
    
            //Reset userType, username, and id only if this is the first message to be received
            let userType = this.state.userType;
            let username = this.state.username;
            let id = this.state.id;
            if (userType === null) {
                userType = message.user_type;
                username = message.username;
                id = message.id;
            }
    
            this.setState({
                userType: userType,
                username: username,
                id: id,
                players: message.players,
                startingChips: message.players[0].chips
            })
        } else {
            //Messages updating the game state
            console.log(e.detail.message);
            let newState = e.detail.message.state;
            if (e.detail.message.type === 'endGame') {
                newState.winner = e.detail.message.winner;
            }
            this.setState(newState);
        }
    }

    otherPlayers() {
        //Returns an array containing all players but you in their seated order

        //Return an empty array if there is only one player
        if (this.state.players.length <= 1) {
            return []
        }

        let currentNode = this.state.players[this.state.players[this.state.id].next];
        let output = []

        while (currentNode.id !== this.state.id) {
            output.push(currentNode);
            currentNode = this.state.players[currentNode.next];
        }

        return output;
    }

    submitBet (bet) {
        this.props.socket.send({
            'type': 'bet',
            'bet': bet
        })
    }

    submitCall () {
        this.props.socket.send({
            'type': 'call'
        })
    }

    submitFold () {
        this.props.socket.send({
            'type': 'fold',
            'id': this.state.id
        })
    }

    render() {
        if (this.state.id === null) {
            return (<div>Joining game</div>)
        }

        console.log(this.state)
        return (
            <div className="game">
                <div>
                    GAME
                </div>

                <p></p>

                <table>
                    <tr>
                    {this.otherPlayers().map(player => (
                        <td><Player player={player} dealer={(player.id === this.state.dealer)}/></td>
                    ))}
                    </tr>
                </table>

                <p> </p>

                {this.state.winner ? 
                    <Winner username={this.state.players[this.state.winner].player}/> :
                    <Table table={this.state.table} pot={this.state.pot} />
                }

                <p> </p>

                <div>
                    {console.log("hand", this.state.hand)}
                    <Me
                        data={this.state.players[this.state.id]}
                        dealer={(this.state.id === this.state.dealer)}
                        hand={this.state.hand ? this.state.hand : []}
                        blind={this.state.blind}
                        currentBet={this.state.currentBet}
                        submitBet={this.submitBet.bind(this)}
                        submitFold={this.submitFold.bind(this)}
                        myTurn={this.state.listening && this.state.id === this.state.currentPlayer}
                        startingChips={this.state.startingChips}
                        playerNum={this.state.players.length}
                    />
                </div>

                <p> </p>

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