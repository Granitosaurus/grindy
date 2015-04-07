import random
import re

from colorama import Fore

from grindy.rating.rating_settings import HINT_COVERAGE
from grindy.utils import print_color


SKIP = 0

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
    :arg skip|s: skips question
    :arg hint|h: prints a hint
    :arg rating|r: prints current rating
    :arg times|t: prints how many times the question was answered
    :arg last_run|lr: prints when was the Last Run of the question
    :arg delete|del: deletes question
    :arg set_rating|setr <value>: sets rating to provided value
    :arg set_question|setq <value>: sets question to provided value
    :arg set_answer|seta <value>: sets answer to provided value
    :arg set_hint|seth <value>: changes the hint of the question

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
            if arg in ['hint', 'h']:
                print_color('Hint: {}'.format(question.hint
                                              or generate_hint(question.answer)
                                              if grindy.auto_hints else ''), Fore.YELLOW)
                continue
            if arg in ['rating', 'r']:
                print_color('Rating: {}'.format(question.rating), Fore.YELLOW)
                continue
            if arg in ['skip', 's']:
                print_color('Skipping question', Fore.RED)
                return SKIP
            if arg in ['times', 't']:
                print_color('Times: {}'.format(question.times), Fore.YELLOW)
                continue
            if arg in ['last_run', 'l']:
                print_color('Last Run: {}'.format(question.last_run), Fore.YELLOW)
                continue
            if arg in ['delete', 'del']:
                if 'y' not in input('Are you sure you want to delete this question? (y/n)').lower():
                    continue
                grindy.deck.questions.remove(question)
                print_color('question "{}" deleted'.format(question.question), Fore.RED)
                return SKIP  # return 0 to skip question
            if arg in ['set_hint', 'seth']:
                print_color('Setting question hint to "{}"'.format(value), Fore.YELLOW)
                question.hint = value
                continue
            if arg in ['set_rating', 'setr']:
                try:
                    value = int(value)
                except ValueError:
                    print_color('value must be integer')
                    continue
                old_rating = question.rating
                question.rating = value if question.rating <= 100 else 100
                print_color('rating changed: ({}->{})'.format(old_rating, question.rating), Fore.YELLOW)
                continue
            if arg in ['set_question', 'setq']:
                old_question = question.question
                question.question = value
                print_color('question changed: ("{}"->"{}")'.format(old_question, question.question), Fore.YELLOW)
                continue
            if arg in ['set_answer', 'seta']:
                old_answer = question.answer
                question.answer = value
                print_color('answer changed: ("{}"->"{}")'.format(old_answer, question.answer), Fore.YELLOW)
                return 0
            print('Unknown argument {}'.format(arg))
            print(HELP)
        if found_arguments:
            return sinput(text, question, grindy)
    return value