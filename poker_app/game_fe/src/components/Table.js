import React from 'react';
import Chips from './Chips';
import Card from './Card';
import '../css/Table.css';

const Table = props => (
    <div className='tableContainer'>
        <div className='pot'>
            <Chips
                chips={props.pot}
                startingChips={props.startingChips}
                playerNum={props.playerNum}
            />
            <div className='potLabel'>
                {props.pot > 0 ? props.pot : ''}
            </div>
        </div>
        <div className='tableCards'>
            {props.table.map (card => (
                <div className='tableCard'>
                    <Card
                        card={card}
                        fontSize='3.6'
                        borderRadius='10px'
                    />
                </div>
            ))}
        </div>
    </div>
)

export default Table;