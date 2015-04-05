import os
import re
from grindy.deck import Question, Deck
from grindy import decks
HINT_COVERAGE = 30


def make_deck(save_location, name):
    """CLI for deck creation
    :param save_location: where the deck will be saved i.e. home/grindy/decks
    :param name: name of the deck
    """
    questions = []
    try:
        while True:
            question = input('Q: ')
            kwargs = parse_input(input('A: '))
            kwargs['question'] = question
            questions.append(Question(kwargs))
    except (KeyboardInterrupt, EOFError):
        name = name + '.json' if not name.endswith('.json') else name
        save_path = os.path.join(save_location, name)
        deck = Deck(save_path, questions)
        print('deck {} has been saved!'.format(name.replace('.json', '')))
        deck.save_deck()


def parse_input(text):
    """reads user input for arguments
    :param text: user input.
    :return dictionary of arguments.
    """
    found_arguments = re.findall('\B-+([^\b|^\s]+)([^-]+)', text)
    arguments = {k: v.strip() for k, v in found_arguments}
    arguments['answer'] = re.split('|'.join(['-'+arg for arg, value in found_arguments]), text)[0]
    return arguments

    # make_deck('alphabet2')
    # print(os.path.dirname(decks.__file__))
    # print(parse_input('january --hint starts with j -rating 10'))