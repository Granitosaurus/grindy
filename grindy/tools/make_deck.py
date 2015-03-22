import os
import re
from grindy.deck import Question, Deck

HINT_COVERAGE = 30


def make_deck(name):
    questions = []
    try:
        while True:
            question = input('Q: ')
            kwargs = parse_input(input('A: '))
            kwargs['question'] = question
            questions.append(Question(kwargs))
    except (KeyboardInterrupt, EOFError):
        name = name + '.json' if not name.endswith('.json') else name
        save_location = os.path.join(os.path.dirname(decks.__file__), name)
        deck = Deck(save_location, questions)
        print('deck {} has been saved!'.format(name.replace('')))
        deck.save_deck()


def parse_input(text):
    found_arguments = re.findall('\B-+([^\b|^\s]+)([^-]+)', text)
    arguments = {k: v.strip() for k, v in found_arguments}
    arguments['answer'] = re.split('|'.join(['-'+arg for arg, value in found_arguments]), text)[0]
    return arguments

    # make_deck('alphabet2')
    # print(os.path.dirname(decks.__file__))
    # print(parse_input('january --hint starts with j -rating 10'))