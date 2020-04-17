"""methods to preprocess hands for validation"""

class PreProcessor():

    face_cards = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    @classmethod
    def preprocess (cls, hands, table):
        """Main preprocessing method; returns preprocessed hands"""
        hands = cls.create_hands(hands, table)
        for player_id in hands:
            hands[player_id]['data'] = cls.preprocess_hand(hands[player_id]['cards'])
        return hands
        
    @classmethod
    def create_hands (cls, hands, table):
        """Create the seven-card hands from each player's pocket and the table"""
        output = {}
        for player_id in hands:
            output[player_id] = {
                'cards': table + hands[player_id]
            }
            cls.sort_cards(output[player_id]['cards'])
        return output

    @classmethod
    def preprocess_hand(cls, hand):
        """Preprocess an individual hand"""
        output = {}
        output['sets'] = cls.preprocess_sets(hand)
        output['flushes'] = cls.preprocess_flushes(hand)
        return output

    @classmethod
    def preprocess_sets(cls, hand):
        """find sets in a hand"""
        cards_by_num = {}
        sets = {
            'pairs': [],
            'threes': [],
            'fours': []
        }
        set_tracker = []
        for idx, card in enumerate(hand):
            if idx == 0 or card[0] != hand[idx - 1][0]:
                if len(set_tracker) == 2:
                    sets['pairs'].append(set_tracker.copy())
                elif len(set_tracker) == 3:
                    sets['threes'].append(set_tracker.copy())
                elif len(set_tracker) == 4:
                    sets['fours'].append(set_tracker.copy())
                set_tracker = [card]
            else:
                set_tracker.append(card)

        if len(set_tracker) == 2:
            sets['pairs'].append(set_tracker.copy())
        elif len(set_tracker) == 3:
            sets['threes'].append(set_tracker.copy())
        elif len(set_tracker) == 4:
            sets['fours'].append(set_tracker.copy())

        return sets

    @classmethod
    def preprocess_flushes(cls, hand):
        """find flushes"""
        cards_by_suit = {
            'D': [],
            'C': [],
            'H': [],
            'S': []
        }

        for card in hand:
            print(card[1])
            cards_by_suit[card[1]].append(card)

        print(cards_by_suit)
        for suit, cards in cards_by_suit.items():
            if len(cards) >= 5:
                return cards
        return []

    @classmethod
    def preprocess_straights(cls, hand):
        """find straights"""
        straight = []
        last_card = None
        if hand[-1][0] == 'A':
            last_card = 1
        for card in hand:
            if last_card is None:
                last_card = int(card[0])
            elif int(card[0]) == last_card + 1:
                pas

    @classmethod
    def sort_cards(cls, hand):
        """Sort cards in a hand by value"""
        hand.sort(key=cls.convert_face_card)

    @classmethod
    def convert_face_card(cls, card):
        """Convert a face card to its numerical value"""
        return cls.face_cards[card[0]]
