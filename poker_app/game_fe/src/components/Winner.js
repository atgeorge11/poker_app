import React from 'react';

const Winner = props => (
    <div style={{
        position: 'absolute',
        top: '40vh',
        fontSize: '30px',
        color: 'yellow',
        fontWeight: 'bold',
        textAlign: 'center',
        width: '100%'
    }}>
        {props.username} wins!
    </div>
)

export default Winner;