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
            {props.dealer ? "Dealer" : ""}
        </div>
    </div>
)

export default Player;