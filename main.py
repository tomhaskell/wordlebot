import click
import logging
from random import choice
from game import Game


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


def _readfile(name: str) -> list[str]:
    with open(name, 'r') as file:
        words = file.read().splitlines()
    return words


if __name__ == '__main__':
    cli()
