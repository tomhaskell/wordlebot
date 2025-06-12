import logging
from enum import Enum


class Game:
    def __init__(self, answer):
        self.__answer = answer
        self.counter = 0
        self.state = Game.State.PLAYING

    def _score(self, word):
        res = [0, 0, 0, 0, 0]
        matches = []

        # check for matching letters
        for i in range(5):
            if word[i] == self.__answer[i]:
                res[i] = 2
                matches.append(word[i])

        # check for correct letters, wrong place
        for i in range(5):
            # check not already matched
            if res[i] > 0:
                continue
            char = word[i]
            # check number of occurances of letter
            word_count = word.count(char)
            answer_count = self.__answer.count(char)
            matches_count = matches.count(char)
            # letter doesn't occur in answer
            if answer_count == 0:
                continue
            # letter occurs in answer more times than in guess
            elif answer_count >= word_count:
                res[i] = 1
                matches.append(char)
            # letter occurs more times than already matched (shows partial match against first x occurances)
            elif answer_count > matches_count:
                res[i] = 1
                matches.append(char)

        return res

    def guess(self, word):
        self.counter += 1
        sc = self._score(word)
        total = sum(sc)
        if total == 10:
            self.state = Game.State.WIN
            logging.debug(f'Game win - {self.counter} guesses')
        elif self.counter >= 6:
            self.state = Game.State.LOSE
            logging.debug(f'Game lose - {self.counter} guesses')
        else:
            logging.debug(
                f'guess {self.counter}: \'{word}\' == \'{self.__answer}\' {sc}')

        return Game.Response(sc, total, self.counter)

    def reveal(self) -> str:
        self.state = Game.State.LOSE
        return self.__answer

    class State(Enum):
        PLAYING = 1
        WIN = 2
        LOSE = 3

    class Response:
        def __init__(self, scores, total, count):
            self.scores = scores
            self.total = total
            self.count = count
