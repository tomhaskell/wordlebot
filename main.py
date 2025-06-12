import click
import logging
from random import choice
from game import Game
from wordle_ai import WordleAI
from ai.random import RandomAI
from ai.simple import SimpleAI


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

    pass


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
@click.pass_context
@click.argument('ai', nargs=1, type=click.STRING)
def ai(ctx, ai: str):
    words = ctx.obj['word_list']
    game = ctx.obj['game']

    if ai == 'random':
        play_ai(game, words, RandomAI(words))
    elif ai == 'simple':
        play_ai(game, words, SimpleAI(words))


def _readfile(name: str) -> list[str]:
    with open(name, 'r') as file:
        words = file.read().splitlines()
    return words


def play_ai(game, words, ai: WordleAI):
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

    for g in guess_history:
        print(f'{g[0]} {''.join(str(i) for i in g[1])}')
    if game.state == Game.State.WIN:
        print(f'Well done! The AI found the Wordle in {game.counter} guesses')
    else:
        print(f'The word was: {game.reveal()}. Better luck next time AI!')


if __name__ == '__main__':
    cli()
