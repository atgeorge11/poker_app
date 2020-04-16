import React from 'react';

class BetSetter extends React.Component{
    constructor(props) {
        super(props);

        console.log(props);

        this.state = {
            digits: this.processNumber(props.blind)
        }
    }

    processDigits (digits) {
        console.log(digits);
        let sum = "";
        for (let i = 0; i < digits.length; i++) {
            sum += digits[i];
        }
        return sum;
    }

    processNumber (number) {
        let numberAsString = JSON.stringify(number);
        console.log(numberAsString);

        //Add the correct number of zeroes to the front
        let addedZeroes = "";
        const numberOfZeroes = JSON.stringify(this.props.chips).length - numberAsString.length;
        for (let i = 0; i < numberOfZeroes; i++) {
            addedZeroes += "0";
        }
        numberAsString = addedZeroes + numberAsString;

        let digits = [];
        for (let i = 0; i < numberAsString.length; i++) {
            digits.push(numberAsString[i]);
        }
        return digits;
    }

    increase (idx) {
        console.log(this.state.digits);
        let newDigits = [];
        for (let i = 0; i < this.state.digits.length; i++) {
            newDigits.push(this.state.digits[i])
        }
        newDigits[idx]++;
        newDigits[idx] = newDigits[idx] % 10;
        let newTotal = this.processDigits(newDigits);
        console.log(newTotal);
        if (newTotal <= this.props.chips && newTotal >= this.props.blind) {
            this.setState({
                digits: newDigits
            });
        } else if (newTotal >= this.props.blind) {
            this.setState({
                digits: this.processNumber(this.props.chips)
            })
        }
    }

    decrease (idx) {
        let newDigits = [];
        for (let i = 0; i < this.state.digits.length; i++) {
            newDigits.push(this.state.digits[i])
        }
        newDigits[idx]--;
        if (newDigits[idx] < 0) {
            newDigits[idx] = 9;
        }
        let newTotal = this.processDigits(newDigits);
        console.log(newTotal);
        if (newTotal <= this.props.chips && newTotal >= this.props.blind) {
            this.setState({
                digits: newDigits
            });
        } else if (newTotal <= this.props.chips) {
            this.setState({
                digits: this.processNumber(this.props.blind)
            })
        }
    }

    render () {
        return (
            <div>
                <table>
                    <tr>
                        {this.state.digits.map( (digit, idx) => (
                            <th onClick={(() => {this.increase(idx)})}>
                                ^
                            </th>
                        ))}
                    </tr>
                    <tr>
                        {this.state.digits.map(digit => (
                            <th>
                                {digit}
                            </th>
                        ))}
                    </tr>
                    <tr>
                        {this.state.digits.map( (digit, idx) => (
                            <th onClick={(() => {this.decrease(idx)})}>
                                v
                            </th>
                        ))}
                    </tr>
                </table>
                <button onClick={() => {this.props.submitBet(this.processDigits(this.state.digits))}}>BET</button>
                <button onClick={this.props.cancel}>Cancel</button>
            </div>
        )
    }
}

export default BetSetter;