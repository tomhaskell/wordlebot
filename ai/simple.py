import logging
from wordle_ai import WordleAI
from random import choice


class SimpleAI(WordleAI):
    """
    SimpleAI uses a basic rule-based approach. It starts with a random word and then chooses the
    next word based on the results
    """

    def __init__(self, words):
        super().__init__(words)

    def next_guess(self, previous_guesses) -> str:
        # is this the first guess?
        if len(previous_guesses) == 0:
            return self._first_word()
        else:
            intel = SimpleAI.WordleIntel(previous_guesses)
            return self._calc_word(intel)

    def _first_word(self) -> str:
        return choice(self.words)

    def _calc_word(self, intel) -> str:
        logging.debug(f'Intel: {intel}')
        poss_words = list(filter(intel.match, self.words))
        logging.debug(f'possible words: {len(poss_words)}')
        if len(poss_words) < 1:
            logging.error('No possible words - random guess time!')
            return choice(self.words)
        return choice(poss_words)

    class WordleIntel:
        def __init__(self, previous_guesses):
            self.matches = [''] * 5
            self.nonmatches = []
            self.partialmatches = []
            self.guessed_words = []
            for guess in previous_guesses:
                word = guess[0]
                self.guessed_words.append(word)
                scores = guess[1]
                for i in range(5):
                    char = word[i]
                    s = scores[i]
                    if s == 2:
                        self.matches[i] = char
                    elif s == 1:
                        self.partialmatches.append(char)
                    elif (not char in self.matches) & (not char in self.partialmatches):
                        self.nonmatches.append(char)

        def match(self, word) -> bool:
            """
            Returns whether the provided word is a possible match, based on the current known intel
            """
            # check if word already guessed
            if word in self.guessed_words:
                return False
            for i in range(5):
                char = word[i]
                # check for nonmatches
                if char in self.nonmatches:
                    return False
                # check for non matches
                if (not self.matches[i] == '') & (not char == self.matches[i]):
                    return False

            for m in self.partialmatches:
                if not m in word:
                    return False

            return True

        def __str__(self) -> str:
            return f'matches: {self.matches}, partials: {self.partialmatches}, nonmatches: {self.nonmatches}'
