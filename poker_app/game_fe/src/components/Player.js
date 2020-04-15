import React from 'react';

const Player = props => (
    <div>
        <div>
            {props.player.player}
        </div>
        <div>
            {props.player.chips}
        </div>
        <div>
            {props.dealer ? "Dealer" : " "}
        </div>
        <p> </p>
        <div>
            {props.player.bet === 0 ? " " : props.player.bet}
        </div>
    </div>
)

export default Player;