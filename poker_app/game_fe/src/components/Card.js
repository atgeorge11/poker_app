import React from 'react';

const Card = props => (
    <div>
        <img
            src={'https://taylor-poker.s3.amazonaws.com/' + props.card + '.jpg'}
            style={{
                height: '90%',
                width: '90%',
                display: 'block',
                marginLeft: 'auto',
                marginRight: 'auto',
                marginTop: 'auto',
                marginBottom: 'auto'
            }}
        />
    </div>
)

export default Card;