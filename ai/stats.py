import logging
from wordle_ai import WordleAI
from copy import deepcopy


class StatsAI(WordleAI):
    """
    StatsAI performs a statistical analysis of all possible words to assign a probability to each
    letter occurring in each position and uses that to calculate a score for a each word. The
    probability is updated based on the guesses (i.e. matched letter = 100%) to produce new scores.
    The word with the heighest score is chosen each time.
    """

    def __init__(self, words):
        super().__init__(words)
        self.letter_occurances = [{}, {}, {}, {}, {}]
        self.total_occurances = {}
        self.train()

    def train(self):
        # count occurances of letters in each position
        letter_occurances = [{}, {}, {}, {}, {}]
        # count total occurances of letters across all positions
        total_occurances = {}
        for word in self.words:
            for i in range(5):
                char = word[i]
                if not char in letter_occurances[i].keys():
                    letter_occurances[i][char] = 1
                else:
                    letter_occurances[i][char] += 1
                if not char in total_occurances.keys():
                    total_occurances[char] = 1
                else:
                    total_occurances[char] += 1

        _max = max(total_occurances.values())
        # normalise total_occurances to 0-1 (1 being most frequent)
        total_occurances = dict(
            map(lambda kv: (kv[0], float(kv[1])/_max), total_occurances.items()))
        # sort (not stricly necessary, but easier for debugging)
        self.total_occurances = {k: v for k, v in sorted(
            total_occurances.items(), key=lambda x: x[1], reverse=True)}

        logging.debug(total_occurances)

        for i in range(5):
            # normalise 0-1 and multiply by total occurances
            _max = max(letter_occurances[i].values())
            letter_occurances[i] = dict(
                map(lambda kv: (kv[0], (float(kv[1]) / _max) * total_occurances[kv[0]]), letter_occurances[i].items()))

            # sort
            self.letter_occurances[i] = {k: v for k, v in sorted(
                letter_occurances[i].items(), key=lambda x: x[1], reverse=True)}

        logging.debug(self.letter_occurances)

    def next_guess(self, previous_guesses: list[tuple[str, list[int]]]) -> str:
        # update scores based on previous guesses
        letter_occurances = deepcopy(self.letter_occurances)
        total_occurances = deepcopy(self.total_occurances)
        matched_letters = []
        found_letters = []
        for g in previous_guesses:
            guess = g[0]
            scores = g[1]
            for i in range(5):
                c = guess[i]
                s = scores[i]

                if s == 2:
                    letter_occurances[i][c] = 1.0
                    total_occurances[c] = 1.0
                    matched_letters.append(c)
                elif s == 1:
                    letter_occurances[i][c] = 0.0
                    total_occurances[c] = 1.0
                    found_letters.append(c)
                else:
                    letter_occurances[i][c] = 0.0
                    if (not c in matched_letters) & (not c in found_letters):
                        total_occurances[c] = 0.0

        # score words based on occurance values
        word_scores = {}
        for word in self.words:
            word_scores[word] = sum(
                list(map(lambda x: letter_occurances[x][word[x]] * total_occurances[word[x]], range(5))))

        # 0 words that have already been guessed
        for g in previous_guesses:
            w = g[0]
            word_scores[w] = 0

        # sort
        word_scores = {k: v for k, v in sorted(
            word_scores.items(), key=lambda x: x[1], reverse=True)}

        logging.debug(list(word_scores.items())[0:10])

        return list(word_scores.keys())[0]
