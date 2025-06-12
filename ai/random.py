from wordle_ai import WordleAI
from random import choice


class RandomAI(WordleAI):
    """
    RandomAI is the dumbest AI - it just picks a completely random word for each guess, ignoring
    previous answers and results. Really it's just here to test the AI gameplay with.
    """

    def __init__(self, words):
        super().__init__(words)

    def next_guess(self, previous_guesses) -> str:
        return choice(self.words)
