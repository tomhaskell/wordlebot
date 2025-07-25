import click
import logging
from random import choice, shuffle
from statistics import fmean
from game import Game
from wordle_ai import WordleAI
from ai.random import RandomAI
from ai.simple import SimpleAI
from ai.stats import StatsAI


@click.group()
@click.option('--debug / --no-debug', default=False, help="Enable debug logging")
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    # read files
    answers = _readfile('wordle-answers.txt')
    ctx.obj['word_list'] = _readfile('valid-wordle-words.txt')

    # pick answer word
    answer = choice(answers)
    ctx.obj['game'] = Game(answer)
    ctx.obj['answers'] = answers


@cli.command()
@click.pass_context
def play(ctx):
    words = ctx.obj['word_list']
    game = ctx.obj['game']

    while game.state == Game.State.PLAYING:
        guess = input('Guess:  ').lower()
        # validate input
        if len(guess) < 5 | len(guess) > 5:
            print('words must be 5 characters, try again')
        elif not guess in words:
            print('invalid word, try again')
        else:
            res = game.guess(guess)
            scores = ''.join(str(i) for i in res.scores)
            print(f'Result: {scores}')

    if game.state == Game.State.WIN:
        print(f'Well done! You found the Wordle in {game.counter} guesses')
    else:
        print(f'The word was: {game.reveal()}. Better luck next time!')


@cli.command(help="get an AI to play the game")
@click.argument('ai', nargs=1, type=click.STRING)
@click.option('--interactive', is_flag=True, help="enable interactive mode")
@click.pass_context
def ai(ctx, ai: str, interactive: bool):
    words = ctx.obj['word_list']
    game = ctx.obj['game']

    ai_engine = _getAIEngine(ai)

    if interactive:
        play_interactive(words, ai_engine(words))
    else:
        play_ai(game, words, ai_engine(words))


@cli.command(help="test an AI over the complete set of answers")
@click.argument('ai', nargs=1, type=click.STRING)
@click.pass_context
def test(ctx, ai: str):
    words = ctx.obj['word_list']
    answers = ctx.obj['answers']

    wins = 0
    guesses = []

    # create AI engine - the same instance is used for all games to prevent retraining every time
    ai_engine = _getAIEngine(ai)(words)

    shuffle(answers)
    for a in answers:
        game = Game(a)
        (state, gs) = play_ai(game, words, ai_engine, False)
        if state == Game.State.WIN:
            wins += 1
            guesses.append(gs)

    print(f'{wins} wins / {len(answers)} ({round(wins/len(answers), 3)*100}%), average guesses: {round(fmean(guesses), 2)}')


def _readfile(name: str) -> list[str]:
    with open(name, 'r') as file:
        words = file.read().splitlines()
    return words


def _getAIEngine(ai: str):
    if ai == 'random':
        ai_engine = RandomAI
    elif ai == 'simple':
        ai_engine = SimpleAI
    elif ai == 'stats':
        ai_engine = StatsAI
    else:
        raise RuntimeError(f'Invalid AI engine: \'{ai}\'')

    return ai_engine


def play_ai(game, words, ai: WordleAI, print_result: bool = True) -> tuple[Game.State, int]:
    guess_history = []
    while game.state == Game.State.PLAYING:
        guess = ai.next_guess(guess_history)
        # validate input
        if len(guess) < 5 | len(guess) > 5:
            raise RuntimeError(
                'words must be 5 characters - is the AI broken?')
        elif not guess in words:
            raise RuntimeError(
                'invalid word - does the AI need retraining with a new word set?')
        else:
            res = game.guess(guess)
            scores = ''.join(str(i) for i in res.scores)
            logging.debug(f'{guess}: {scores}')
            guess_history.append((guess, res.scores))

    if print_result:
        for g in guess_history:
            print(f'{g[0]} {''.join(str(i) for i in g[1])}')
        if game.state == Game.State.WIN:
            print(
                f'Well done! The AI found the Wordle in {game.counter} guesses')
        else:
            print(f'The word was: {game.reveal()}. Better luck next time AI!')

    return (game.state, game.counter)


def play_interactive(words, ai: WordleAI):
    logging.debug('Starting interactive AI session...')
    guess_history = []
    score_total = 0
    counter = 0
    while (score_total < 10) & (counter < 6):
        guess = ai.next_guess(guess_history)
        counter += 1
        # validate input
        if len(guess) < 5 | len(guess) > 5:
            raise RuntimeError(
                'words must be 5 characters - is the AI broken?')
        elif not guess in words:
            raise RuntimeError(
                'invalid word - does the AI need retraining with a new word set?')
        else:
            scores = input(f'guess: {guess} | enter scores: ')
            scores_list = list(int(x) for x in scores)
            score_total = sum(scores_list)
            guess_history.append((guess, scores_list))
        logging.debug(
            f'counter: {counter}, guess: {guess} score_total: {score_total}')

    if score_total == 10:
        print(f'Well done! The AI found the Wordle in {counter} guesses')
    else:
        print(f'The AI failed to guess the word. Better luck next time AI!')


if __name__ == '__main__':
    cli()
