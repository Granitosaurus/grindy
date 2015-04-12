import os
import re
from grindy.deck import Question, Deck

HINT_COVERAGE = 30


def make_deck(save_location, name, update=False, list_of_tuples=None):
    """CLI for deck creation and update
    :param save_location: where the deck will be saved i.e. home/grindy/decks
    :param name: name of the deck
    :param list_of_tuples: instead of direct input take this as input where list_of_tuples is [(question, answer),...]
    """
    questions = []
    name = name + '.json' if not name.endswith('.json') else name
    save_path = os.path.join(save_location, name)
    if update:
        deck = Deck(save_path)

    # Input either from argument
    if list_of_tuples:
        for q in list_of_tuples:
            questions.append(Question(question=q[0], answer=q[1]))
    # Or direct input
    else:
        try:
            while True:
                question = input('Q: ')
                kwargs = parse_input(input('A: '))
                kwargs['question'] = question
                questions.append(Question(kwargs))
        except (KeyboardInterrupt, EOFError):
            pass

    if update:
        deck.questions += questions
    else:
        deck = Deck(save_path, questions)
    deck.save_deck()
    print('deck {} has been saved!'.format(name.replace('.json', '')))


def parse_input(text):
    """reads user input for arguments
    :param text: user input.
    :return dictionary of arguments.
    """
    found_arguments = re.findall('\B-+([^\b|^\s]+)([^-]+)', text)
    arguments = {k: v.strip() for k, v in found_arguments}
    arguments['answer'] = re.split('|'.join(['-' + arg for arg, value in found_arguments]), text)[0]
    return arguments
