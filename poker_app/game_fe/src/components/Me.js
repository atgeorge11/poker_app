import React, { useState } from 'react';
import BetSetter from './BetSetter';

const Me = props => {

    console.log(props.myTurn);
    
    const [betting, setBetting] = useState(false);
    let menu = (<div></div>);

    if (props.myTurn) {
        menu = (
            <div>
                <button onClick={props.submitCall}>Call</button>
                <button onClick={() => {setBetting(true)}}>Raise</button>
                <button onClick={props.submitFold}>Fold</button>
            </div>
        );
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
        
        {!betting ?
            menu : 
            <BetSetter
                blind={props.blind}
                chips={props.data.chips}
                submitBet={props.submitBet}
                cancel={() => {setBetting(false)}}
            />
        }

    </div>
)}

export default Me;