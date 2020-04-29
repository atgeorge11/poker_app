import React from 'react';

const Chips = props => {
    let chips = props.chips;
    let startingChips = props.startingChips;
    let playerNum = props.playerNum;

    let maxChips = startingChips * playerNum;

    let stackSize = maxChips / 7;

    let stacks = [0, 0, 0, 0, 0, 0, 0];

    let styles = [];
    let stylesTop = [];
    let stylesBottom = [];

    for (let i = 0; i < stacks.length; i++) {
        if (chips > stackSize) {
            stacks[i] = 95;
            chips -= stackSize
        } else if (chips > 0) {
            stacks[i] = 95 * chips / stackSize;
            chips = 0
        }
    }

    for (let i = 0; i < 7; i++) {
        if (stacks[i] > 0) {
            styles.push({
                width: '100%',
                height: stacks[i] + '%',
                position: 'absolute',
                bottom: '0',
                backgroundColor: 'red',
                border: '1px solid black',
            });
            stylesTop.push({
                backgroundColor: 'red',
                borderRadius: '50%',
                position: 'absolute',
                bottom: (stacks[i]) + '%',
                height: '10%',
                width: '100%',
                border: '1px solid black'
            });
            stylesBottom.push({
                backgroundColor: 'red',
                borderRadius: '50%',
                position: 'absolute',
                top: '95%',
                height: '10%',
                width: '100%',
                borderBottom: '1px solid black',
                borderLeft: '1px solid black',
                borderRight: '1px solid black'
            });
        } else {
            styles.push({});
            stylesTop.push({});
            stylesBottom.push({});
        }
    }

    return (
        <div style={{
            width: '50%',
            height: '50%',
            position: 'absolute',
            top: '50%',
            left: '25%'
        }}>
            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '16%',
                bottom: '20%',
            }}>
                <div style={styles[0]}></div>
                <div style={stylesTop[0]}></div>
                <div style={stylesBottom[0]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '48%',
                bottom: '20%',
            }}>
                <div style={styles[1]}></div>
                <div style={stylesTop[1]}></div>
                <div style={stylesBottom[1]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '0%',
                bottom: '10%',
            }}>
                <div style={styles[2]}></div>
                <div style={stylesTop[2]}></div>
                <div style={stylesBottom[2]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '32%',
                bottom: '10%',
            }}>
                <div style={styles[3]}></div>
                <div style={stylesTop[3]}></div>
                <div style={stylesBottom[3]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '64%',
                bottom: '10%',
            }}>
                <div style={styles[4]}></div>
                <div style={stylesTop[4]}></div>
                <div style={stylesBottom[4]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '16%',
                bottom: '0%',
            }}>
                <div style={styles[5]}></div>
                <div style={stylesTop[5]}></div>
                <div style={stylesBottom[5]}></div>
            </div>

            <div style={{
                position: 'absolute',
                width: '30%',
                height: '80%',
                left: '48%',
                bottom: '0%',
            }}>
                <div style={styles[6]}></div>
                <div style={stylesTop[6]}></div>
                <div style={stylesBottom[6]}></div>
            </div>

        </div>
    )

}

export default Chips;