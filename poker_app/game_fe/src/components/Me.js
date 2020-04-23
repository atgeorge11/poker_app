import React, { useState } from 'react';
import BetSetter from './BetSetter';

const Me = props => {

    let menu = (<div></div>);

    if (props.myTurn) {
        menu = (
            <div>
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
        
        {/* {!betting ?
            menu : 
            <BetSetter
                blind={props.blind}
                chips={props.data.chips}
                currentBet={props.currentBet}
                submitBet={props.submitBet}
                cancel={() => {setBetting(false)}}
            />
        } */}

    </div>
)}

export default Me;