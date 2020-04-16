import React from 'react';

const Table = props => (
    <div>
        <p> </p>
        <div>
            {props.table.map (card => card + " ")}
        </div>
        <div>
            {props.pot}
        </div>
        <p> </p>
    </div>
)

export default Table;