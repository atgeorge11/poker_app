from .preprocessor import PreProcessor
from .converter import Converter

class Validator():

    """validate a hand"""
    @classmethod
    def validate (cls, hands, table):
        preprocessed_hands = PreProcessor.preprocess(hands, table)
        scores = {}
        for player_id, hand in preprocessed_hands.items():
            scores[player_id] = (cls.run_methods(hand))

        return scores

    """Return a straight if one exists in the input cards"""
    @classmethod
    def detect_straight (cls, cards):
        last_value = -1
        straight = []
        if cards[-1][0] == 'A':
            last_value = 1
        for card in cards:
            current_value = int(Converter.convert(card), 16)
            if current_value == last_value + 1:
                if last_value == 1:
                    straight.append(cards[-1])
                straight.append(card)
                last_value = current_value
            elif current_value != last_value:
                if len(straight) >= 5:
                    break
                straight = [card]
                last_value = current_value
        if len(straight) < 5:
            straight = []
        return straight

    """does the hand contain a royal flush"""
    #returns the score if so and None if not
    @classmethod
    def royal_flush (cls, hand):
        flush = hand['data']['flushes']
        if len(flush) == 0:
            return None
        if flush[-1][0] != 'A':
            return None
        if len(cls.detect_straight(flush)) == 0:
            return None
        return '900000'

    """does the hand contain a straight flush"""
    #returns the score if so and None if not
    @classmethod
    def straight_flush (cls, hand):
        flush = hand['data']['flushes']
        if len(flush) == 0:
            return None
        if len(cls.detect_straight(flush)) == 0:
            return None
        firstDigit = '8'
        
        highest = Converter.convert(flush[-1][0])
        second_highest = Converter.convert(flush[-2][0])
        if highest == 'e' and second_highest == '5':
            return firstDigit + second_highest + '0000'
        return firstDigit + highest + '0000'

    """does the hand contain a four-of-a-kind"""
    #returns the score if so and None if not
    @classmethod
    def four_of_a_kind (cls, hand):
        four = hand['data']['sets']['fours']
        if len(four) == 0:
            return None
        firstDigit = '7'
        secondDigit = Converter.convert(four[0][0])
        thirdDigit = None
        idx = 6
        while thirdDigit == None:
            if hand['cards'][idx][0] != four[0][0][0]:
                thirdDigit = Converter.convert(hand['cards'][idx])
            idx -= 1
        return firstDigit + secondDigit + thirdDigit + '000'

    """does the hand contain a full house"""
    #returns the score if so and None if not
    @classmethod
    def full_house (cls, hand):
        sets = hand['data']['sets']
        threes = sets['threes']
        pairs = sets['pairs']

        if (len(threes) == 0 or len(pairs) == 0) and len(threes) < 2:
            return None

        firstDigit = '6'
        secondDigit = Converter.convert(threes[-1][0])

        thirdDigit = None

        if len(threes) > 1:
            thirdDigit = Converter.convert(threes[-2][0])
        else:
            thirdDigit = Converter.convert(pairs[-1][0])

        return firstDigit + secondDigit + thirdDigit + '000'

    """does the hand contain a flush"""
    #returns the score if so and None if not
    @classmethod
    def flush (cls, hand):
        flush = hand['data']['flushes']
        if len(flush) == 0:
            return None
        
        output = '5'

        card_counter = 5
        for card in reversed(flush):
            if card_counter > 0:
                output += Converter.convert(card)
                card_counter -= 1

        return output

    """does the hand contain a straight"""
    #returns the score if so and None if not
    @classmethod
    def straight (cls, hand):
        straight = cls.detect_straight(hand['cards'])
        if len(straight) == 0:
            return None

        firstDigit = '4'
        secondDigit = Converter.convert(straight[-1])
        return firstDigit + secondDigit + '0000'

    """does the hand contain a three-of-a-kind"""
    #returns the score if so and None if not
    @classmethod
    def three_of_a_kind (cls, hand):
        threes = hand['data']['sets']['threes']
        if len(threes) == 0:
            return None
        
        firstDigit = '3'
        secondDigit = Converter.convert(threes[-1][0])

        nextDigits = []
        for card in reversed(hand['cards']):
            if len(nextDigits) < 2 and card[0] != threes[0][0][0]:
                nextDigits.append(Converter.convert(card))

        return firstDigit + secondDigit + nextDigits[0] + nextDigits[1] + '00'

    """does the hand contain a two-pair"""
    #returns the score if so and None if not
    @classmethod
    def two_pair (cls, hand):
        pairs = hand['data']['sets']['pairs']
        if len(pairs) < 2:
            return None

        firstDigit = '2'
        secondDigit = Converter.convert(pairs[-1][0])
        thirdDigit = Converter.convert(pairs[-2][0])

        fourthDigit = None
        for card in reversed(hand['cards']):
            if fourthDigit == None and card != pairs[-1][0] and card != pairs[-1][0]:
                fourthDigit = Converter.convert(card)
        return firstDigit + secondDigit + thirdDigit + fourthDigit + '00'

    """does the hand contain a pair"""
    #returns the score if so and None if not
    @classmethod
    def pair (cls, hand):
        pairs = hand['data']['sets']['pairs']
        if len(pairs) == 0:
            return None
        
        firstDigit = '1'
        secondDigit = Converter.convert(pairs[0][0])

        nextDigits = []
        for card in reversed(hand['cards']):
            if len(nextDigits) < 3 and Converter.convert(card) != Converter.convert(pairs[0][0]):
                nextDigits.append(Converter.convert(card))

        return firstDigit + secondDigit + nextDigits[0] + nextDigits[1] + nextDigits[2] + '0'

    """scores a high card hand"""
    #returns the score
    @classmethod
    def high_card (cls, hand):
        cards = hand['cards']
        output = '0'

        for idx in range(1, 6):
            output += Converter.convert(cards[idx * -1])

        return output
    

    """Calls validator methods in the correct order"""
    @classmethod
    def run_methods (cls, hand):
        validation_methods = {
            '0': cls.high_card,
            '1': cls.pair,
            '2': cls.two_pair,
            '3': cls.three_of_a_kind,
            '4': cls.straight,
            '5': cls.flush,
            '6': cls.full_house,
            '7': cls.four_of_a_kind, 
            '8': cls.straight_flush,
            '9': cls.royal_flush
        }
        
        phase = 9

        score = None

        while (score == None):
            score = validation_methods[str(phase)](hand)
            phase -= 1

        return score

        """        
        {
            '1':{
                'cards': ['3S', '4S', '5S', '6S', '7H', '8S', '9S'],
                'data': {
                    'sets': {
                        'pairs': [],
                        'threes': [],
                        'fours': []
                    },
                    'flushes': ['3S', '4S', '5S', '6S', '8S', '9S']
                }
            },
            '2': {
                'cards': ['3S', '3D', '6S', '7H', '8S', '9S', 'KH'],
                'data': {
                    'sets': {
                        'pairs': [['3S', '3D']],
                        'threes': [],
                        'fours': []
                    },
                    'flushes': []
                    }}, '3': {'cards': ['3S', '6S', '7H', '8S', '9S', 'JC', 'JD'], 'data': {'sets': {'pairs': [['JC', 'JD']], 'threes': [], 'fours': []}, 'flushes': []}}}
        """