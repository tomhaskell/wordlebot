from abc import ABC, abstractmethod


class WordleAI(ABC):
    def __init__(self, words):
        self.words = words

    @abstractmethod
    def next_guess(self, previous_guesses) -> str:
        pass
