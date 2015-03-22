import random
import re

from colorama import Fore

from grindy.rating.rating_manager import rate
from grindy.rating.ratting_settings import HINT_COVERAGE
from grindy.utils import print_color


HELP = '''commands:
-h question hint if available.
-r question rating.
-t times question answered.
-lr last time the question was answered.
'''


def find_arguments(text):
    return re.findall('\B(-[^\b|^\s]+)', text)


def generate_hint(answer):
        obscured = [char for char in re.sub('\w', '*', answer)]
        uncover_amount = round(HINT_COVERAGE * len(answer) / 100)
        for i in range(uncover_amount):
            uncover = random.choice(range(len(answer)))
            if obscured[uncover] != '*':
                continue
            obscured[uncover] = answer[uncover]
        return ''.join(obscured)


def sinput(text, question, grindy):
    value = input(text)
    if '-quit' in value.lower():
        raise KeyboardInterrupt

    if question:
        found_arguments = find_arguments(value)
        for arg in found_arguments:
            if arg == '-h':
                print_color('Hint: {}'.format(question.hint
                                              or generate_hint(question.answer)
                                              if grindy.auto_hints else ''), Fore.YELLOW)
                continue
            if arg == '-r':
                print_color('Rating: {}'.format(question.rating), Fore.YELLOW)
                continue
            if arg == '-t':
                print_color('Times: {}'.format(question.times), Fore.YELLOW)
                continue
            if arg == '-lr':
                print_color('Last Run: {}'.format(question.last_run), Fore.YELLOW)
                continue
            if arg == '-r3':
                print_color('Rated question at 3(Hard)'.format(question.hint), Fore.YELLOW)
                rate(question, 3)
                continue
            if arg == '-r2':
                print_color('Rated question at 2(Medium)'.format(question.hint), Fore.YELLOW)
                rate(question, 2)
                continue
            if arg == '-r1':
                print_color('Rated question at 1(easy)'.format(question.hint), Fore.YELLOW)
                rate(question, 1)
                continue
            print('Unknown argument {}'.format(arg))
            print(HELP)
        if found_arguments:
            return sinput(text, question, grindy)
    return value