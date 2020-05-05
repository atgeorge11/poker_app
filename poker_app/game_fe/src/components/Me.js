import React, { useState } from 'react';
import BetSetter from './BetSetter';
import Chips from './Chips';
import Card from './Card';
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

            <div className='myBetContainer'>
                <div className='myDealer'>
                    {props.dealer ? (
                    <span className="dealerChip"></span>
                    ) : null}
                </div>
                <div className='myBet'>
                        <div className='myBetImage'>
                            <Chips
                                chips={props.data.bet}
                                startingChips={props.startingChips}
                                playerNum={props.playerNum}
                            />
                        </div>
                        <div className='myBetNumber'>
                            {props.data.bet ? props.data.bet : ''}
                        </div>
                </div>
            </div>

            <div className='meTable'>
                    <div className='meTableCell left'>
                        <div className='myChipsImage'>
                            <Chips
                                chips={props.data.chips}
                                startingChips={props.startingChips}
                                playerNum={props.playerNum}
                            />
                        </div>
                        <div className='myChips'>
                            {props.data.chips}
                        </div>
                    </div>
                    <div className='meTableCell right'>
                        {props.hand.map(card => (
                            <div className='myCard'>
                                <Card card={card} fontSize='5.5' borderRadius='10px'/>
                            </div>
                        ))}
                    </div>
            </div>
            <div className='meName'>
                {props.data.player}
            </div>
        </div>
        {menu}
    </div>
)}

export default Me;