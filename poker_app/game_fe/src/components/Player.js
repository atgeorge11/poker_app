import React from 'react';

const Player = props => (
    <div>
        Player
        <div>
            {props.player.player}
        </div>
        <div>
            {props.player.amount}
        </div>
    </div>
)

export default Player;