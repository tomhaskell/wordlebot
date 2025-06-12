# Wordlebot

A command-line version of wordle that can be played manually or used to train an AI

Words lists from: https://github.com/Kinkelin/WordleCompetition/tree/main/data/official

## Manual play
To play the game yourself:

```bash
python main.py play
```

For each guess you make, the result is shown as follows:

0. no match
1. correct letter, wrong location
2. direct match

## AI play
To get an AI to play the game:

```bash
python main.py ai <ai_name>
```

Available AIs:

- `random` - RandomAI is the dumbest AI - it just picks a completely random word for each guess, ignoring
    previous answers and results. Really it's just here to test the AI gameplay with.
- `simple` - SimpleAI uses a basic rule-based approach. It starts with a random word and then chooses the
    next word based on the results

### Interactive mode
Interactive mode allows you to provide the scores to the AI - either based on a word you have thought up
or by entering into a third-party wordle app and relaying the results

```bash
python main.py ai --interactive <ai_name>
```