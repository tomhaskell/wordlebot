from abc import ABC, abstractmethod


class WordleAI(ABC):
    def __init__(self, words):
        self.words = words

    @abstractmethod
    def next_guess(self, previous_guesses: list[tuple[str, list[int]]]) -> str:
        """
        next_guess() returns the next guess the AI has generated.
        When implementing, this method should idempotent (i.e. if called once or multiple times, it
        should produce the same output given the same input) so don't change any underlying data
        structures

        previous_guesses is a list of tuples of the form (word, scores) for the previous guesses
        """
        pass
