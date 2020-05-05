import React from 'react';
import Chips from './Chips';
import Card from './Card';
import '../css/Player.css';

const Player = props => {

    const x = 100 * props.id / props.playerNum + (50 / props.playerNum);
    const y = (200 - Math.sqrt(40000 - (40000 * ((-1 * x + 50) / 50)**2))) / 2;

    return (
    <div style={{
        position: 'absolute',
        left: x + '%',
        top: y + '%',
        width: '50px',
        height: '100px',
        marginLeft: '-25px'
    }}>
        <div className='playerName'>
            {props.player.player}
        </div>
        <div className='playerChips'>
            <Chips
                chips={props.player.chips}
                startingChips={props.startingChips}
                playerNum={props.playerNum + 1}
            />
        </div>
        <div className='playerChipsNum'>
            {props.player.status === 'out' ? 'OUT' : props.player.chips}
        </div>
        {props.player.hand.length === 0 ? '' : (
            <div className='playerCards'>
                <div className='playerCard'>
                    <Card card={props.player.hand[0]} fontSize='2' borderRadius='5px'/>
                </div>
                <div className='playerCard'>
                    <Card card={props.player.hand[1]} fontSize='2' borderRadius='5px'/>
                </div>
            </div>
        )}
        <div className='playerBet'>
            <Chips
                chips={props.player.bet}
                startingChips={props.startingChips}
                playerNum={props.playerNum + 1}
            />
        </div>
        <div className='playerBetNum'>
            {props.player.bet === 0 ? " " : props.player.bet}
        </div>
        <div className='playerDealer'>
            {props.dealer ? <span className='dealer'></span> : " "}
        </div>
    </div>
    )}

export default Player;