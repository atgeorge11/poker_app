import React from 'react';
import '../css/BetSetter.css';

class BetSetter extends React.Component{
    constructor(props) {
        super(props);

        console.log(props);

        let newDigits = Math.min(props.currentBet - props.myBet, props.chips)

        this.state = {
            digits: this.processNumber(newDigits)
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
        
        if (newTotal <= this.props.currentBet - this.props.myBet) {
            this.setState({
                digits: this.processNumber(Math.min(this.props.currentBet - this.props.myBet, this.props.chips))
            })
        } else if (newTotal <= this.props.currentBet - this.props.myBet + this.props.blind) {
            this.setState({
                digits: this.processNumber(Math.min(this.props.currentBet - this.props.myBet + this.props.blind, this.props.chips))
            })
        } else {
            this.setState({
                digits: this.processNumber(Math.min(newTotal, this.props.chips))
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

        if (newTotal <= this.props.currentBet - this.props.myBet) {
            this.setState({
                digits: this.processNumber(Math.min(this.props.currentBet - this.props.myBet, this.props.chips))
            })
        } else if (newTotal <= this.props.currentBet - this.props.myBet + this.props.blind) {
            this.setState({
                digits: this.processNumber(Math.min(this.props.currentBet - this.props.myBet + this.props.blind, this.props.chips))
            })
        } else {
            this.setState({
                digits: this.processNumber(Math.min(newTotal, this.props.chips))
            })
        }
    }

    render () {
        let call = Number(this.processDigits(this.state.digits)) === this.props.currentBet - this.props.myBet ? 'Call' : 'Raise';
        if (Number(this.processDigits(this.state.digits)) === 0) {
            call = "Check";
        } else if (Number(this.processDigits(this.state.digits)) === this.props.chips) {
            call = 'All-In';
        }

        return (
            <div className='betsetterContainer'>
                <table className="betsetter">
                    <tr className="betsetterArrow">
                        {this.state.digits.map( (digit, idx) => (
                            <th onClick={(() => {this.increase(idx)})} className="betsetterCol betsetterClick">
                                ^
                            </th>
                        ))}
                    </tr>
                    <tr className="betsetterNum">
                        {this.state.digits.map(digit => (
                            <th className="betsetterCol">
                                {digit}
                            </th>
                        ))}
                    </tr>
                    <tr className="betsetterArrow">
                        {this.state.digits.map( (digit, idx) => (
                            <th onClick={(() => {this.decrease(idx)})} className="betsetterCol betsetterClick">
                                v
                            </th>
                        ))}
                    </tr>
                </table>
                <div className='betsetterButtons'>
                    <div
                        onClick={() => {this.props.submitBet(this.processDigits(this.state.digits))}}
                        className='betsetterButton betsetterClick'
                    >
                        {call}
                    </div>
                    <div onClick={this.props.submitFold} className='betsetterButton betsetterClick'>Fold</div>
                </div>
                
            </div>
        )
    }
}

export default BetSetter;