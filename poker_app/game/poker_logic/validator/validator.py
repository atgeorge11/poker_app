from .preprocessor import PreProcessor

class Validator():
    """validate a hand"""

    def validate (hands, table):
        preprocessed_hands = PreProcessor.preprocess(hands, table)
        return preprocessed_hands
