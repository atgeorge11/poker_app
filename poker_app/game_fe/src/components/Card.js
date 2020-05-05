import React from 'react';

const Card = props => {
    console.log('card props card', props.card);
    const suits = {
        'D':'♦',
        'H': '♥',
        'C': '♣',
        'S': '♠'
    }

    let suit;
    let num;

    if (props.card[0] === '1' && props.card[1] === '0') {
        suit = props.card[2];
        num = '10';
    } else {
        suit = props.card[1];
        num = props.card[0];
    }

    let color;

    if (suit === 'D' || suit === 'H') {
        color = 'red';
    } else {
        color = 'black';
    }

    if (props.card[0] === 'x') {
        return (
            <img src='https://taylor-poker.s3.amazonaws.com/blue_back.jpg' style={{
                height: '90%',
                width: '90%',
                display: 'block',
                borderRadius: props.borderRadius, 
            }}/>
        )
    }


    return (

    <div style={{
        height: '90%',
        width: '90%',
        display: 'block',
        borderRadius: props.borderRadius,
        backgroundColor: 'white',
        color: color,
        fontSize: props.fontSize + 'vh'
    }}>
        <div>
            {num}
        </div>
        <div>
            {suits[suit]}
        </div>
        {/* <img
            src={'https://taylor-poker.s3.amazonaws.com/' + props.card + '.jpg'}
            style={{
                height: '90%',
                width: '90%',
                display: 'block',
                marginLeft: 'auto',
                marginRight: 'auto',
                marginTop: 'auto',
                marginBottom: 'auto',
                borderRadius: '10px'
            }}
        /> */}
    </div>
    )
}

export default Card;