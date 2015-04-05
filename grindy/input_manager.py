import random
import re

from colorama import Fore

from grindy.rating.rating_settings import HINT_COVERAGE
from grindy.utils import print_color


HELP = '''commands:
-h question hint if available.
-r question rating.
-t times question answered.
-lr last time the question was answered.
-set_rating set rating (0 =< value =< 100)'''


def find_arguments(text):
    """Finds arguments in text
    :param text: text where to look for arguments
    :return a list of tuples of (argument, value)
    """
    return re.findall('\B-+([^\b|^\s]+)(?:\s|)([^-]+|-\d+|)', text)


def generate_hint(answer):
    """Generates hint based on HINT_COVERATE rating setting,
    i.e. HINT_COVERAGE 30 will unveil 30% random letters of the word"""
    obscured = [char for char in re.sub('\w', '*', answer)]
    uncover_amount = round(HINT_COVERAGE * len(answer) / 100)
    for i in range(uncover_amount):
        uncover = random.choice(range(len(answer)))
        if obscured[uncover] != '*':
            continue
        obscured[uncover] = answer[uncover]
    return ''.join(obscured)


def sinput(text, question, grindy):
    """Smart input for question answers which reads the answer for arguments such as --hint
    Currently available arguments:
    :arg quit: quits the program
    :arg h: prints a hint
    :arg r: prints current rating
    :arg set_hint <value>: changes the hint of the question
    :arg t: prints how many times the question was answered
    :arg lr: prints when was the Last Run of the question
    :arg set_rating <value>: sets rating to provided value

    :param text: answer input text.
    :param question: question object.
    :param grindy: grindy program object.
    """
    value = input(text)
    if '-quit' in value.lower():
        raise KeyboardInterrupt

    if question:
        found_arguments = find_arguments(value)
        for arg, value in found_arguments:
            value = value.strip()
            if arg == 'h':
                print_color('Hint: {}'.format(question.hint
                                              or generate_hint(question.answer)
                                              if grindy.auto_hints else ''), Fore.YELLOW)
                continue
            if arg == 'r':
                print_color('Rating: {}'.format(question.rating), Fore.YELLOW)
                continue
            if arg == 'set_hint':
                print_color('Setting question hint to "{}"'.format(value), Fore.YELLOW)
                question.hint = value
                continue
            if arg == 't':
                print_color('Times: {}'.format(question.times), Fore.YELLOW)
                continue
            if arg == 'lr':
                print_color('Last Run: {}'.format(question.last_run), Fore.YELLOW)
                continue
            if arg == 'set_rating':
                try:
                    value = int(value)
                except ValueError:
                    print_color('value must be integer')
                    continue
                old_rating = question.rating
                question.rating = value if question.rating <= 100 else 100
                print_color('rating changed: ({}->{})'.format(old_rating, question.rating), Fore.YELLOW)
                continue
            print('Unknown argument {}'.format(arg))
            print(HELP)
        if found_arguments:
            return sinput(text, question, grindy)
    return value