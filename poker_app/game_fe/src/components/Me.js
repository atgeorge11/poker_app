import React, { useState } from 'react';
import BetSetter from './BetSetter';
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
                />
                <button onClick={props.submitFold}>Fold</button>
            </div>
        )
        
        // (
        //     <div>
        //         <button onClick={props.submitCall}>{allIn ? "All-In" : "Call"}</button>
        //         <button onClick={allIn ? null :() => {setBetting(true)}}>Raise</button>
        //         <button onClick={props.submitFold}>Fold</button>
        //     </div>
        // );
    } 

    return (
    <div>
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