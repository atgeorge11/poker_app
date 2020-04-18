class Converter ():

    cards = {
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '1': 'a',
        'J': 'b',
        'Q': 'c',
        'K': 'd',
        'A': 'e'
    }

    @classmethod
    def convert(cls, card):
        """Convert a face card to its numerical value"""
        return cls.cards[card[0]]
    
