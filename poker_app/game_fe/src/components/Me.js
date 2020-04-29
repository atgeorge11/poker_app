import React, { useState } from 'react';
import BetSetter from './BetSetter';
import Chips from './Chips';
import '../css/Me.css';

const Me = props => {

    let menu = (<div className='menu'></div>);

    if (props.myTurn) {
        menu = (
            <div className='menu'>
                <BetSetter
                    blind={props.blind}
                    chips={props.data.chips}
                    currentBet={props.currentBet}
                    myBet={props.data.bet}
                    submitBet={props.submitBet}
                    submitFold={props.submitFold}
                />
            </div>
        )
    } 

    return (
    <div>
        <div className="meContainer">
            {props.dealer ? (
                <div className="dealerChip"></div>
            ) : null}
            <div>
                {props.data.player}
            </div>
            <div>
                <Chips
                    chips={props.data.chips}
                    startingChips={props.startingChips}
                    playerNum={props.playerNum}
                />
            </div>
            <div>
                {props.data.chips}
            </div>
        </div>

        <div>
            {props.data.bet === 0 ? " " : props.data.bet}
        </div>
        <p> </p>
        <div>
            {props.data.player}
        </div>
        <div>
            {props.data.chips}
        </div>
        <div>
            {props.dealer ? "Dealer" : " "}
        </div>
        <div>
            {props.hand.map(card => (
                <React.Fragment>
                    {console.log(card)}
                    {card} 
                </React.Fragment>
            ))}
        </div>
        {menu}
    </div>
)}

export default Me;