import os
import re
from colorama import Back
from colorama import Fore
from grindy import utils
from grindy.deck import Question, Deck

HINT_COVERAGE = 30


class DeckMaker:
    """
    Deck maker for grindy
    """
    HINT_COVERAGE = 30
    SINPUT_HELP = "possible input arguments:\n" \
                  "-allq: prints all questions in the deck\n" \
                  "-allqa: prints all questions and answers in the deck\n" \
                  "-skip|-s: skips question"

    def __init__(self, save_location, name, update=False, direct_tuple_input=None):
        self.name = name + '.json' if not name.endswith('.json') else name
        self.save_path = os.path.join(save_location, self.name)
        self.direct_tuple_input = direct_tuple_input
        self.questions = []
        if update:
            self.questions = Deck(self.save_path).questions

    def make_deck(self):
        if self.direct_tuple_input:
            self._make_deck_directly()
        else:
            self._make_deck_input()

        deck = Deck(self.save_path, self.questions)
        deck.save_deck()
        print('\ndeck "{}" has been saved!'.format(self.name.replace('.json', '')))

    def _make_deck_directly(self):
        for q in self.direct_tuple_input:
            self.questions.append(Question(question=q[0], answer=q[1]))

    def _make_deck_input(self):
        try:
            while True:
                input_question = self.sinput('{} Q: '.format(len(self.questions) + 1))[0]
                if input_question == 0:
                    print('skipping')
                    continue
                input_question = input_question.strip()
                # checking for duplicates
                if input_question.lower() in (q.question.lower() for q in self.questions):
                    while True:
                        dup_answer = input('Question already exists, do you want to (c)ancel/(a)dd/(o)verride?').lower()
                        if dup_answer in ['c', 'a', 'o']:
                            break
                    if dup_answer == 'c':
                        continue
                    if dup_answer == 'o':
                        self.questions = [q for q in self.questions if q.question != input_question]
                input_kwargs = self.sinput_answer('{} A: '.format(len(self.questions) + 1))
                if input_kwargs['answer'] == 0:
                    print('skipping')
                    continue
                input_kwargs['question'] = input_question
                self.questions.append(Question(input_kwargs))
        except (KeyboardInterrupt, EOFError):
            pass

    def sinput(self, text, restricted=True):
        """reads user input for arguments
        :param text: text for user input.
        :param restricted: restrict input to known arguments.
        :return dictionary of arguments.
        """
        value = input(text)
        found_arguments = re.findall('\B-+([^\b|^\s]+)(?:\s|)([^-]+|-\d+|)', value)
        arguments = {k: v.strip() for k, v in found_arguments}
        for arg in arguments:
            if 'allq' == arg:
                for index, q in enumerate(self.questions):
                    print('{} {}'.format(index + 1, q.question))
                return self.sinput(text)
            if 'allqa' == arg:
                for index, q in enumerate(self.questions):
                    print('{} {}'.format(index + 1, q.question))
                    print('{} {}'.format(index + 1, q.answer))
                return self.sinput(text)
            if arg in ['skip', 's']:
                return 0, arguments
            if restricted:
                print('Unknown argument {}'.format(arg))
        if restricted and arguments:
            print(self.SINPUT_HELP)
            return self.sinput(text, restricted=restricted)
        value = re.split('|'.join(['-+' + arg for arg, _ in arguments]), value)[0]
        return value, arguments

    def sinput_answer(self, text):
        """smart user input for answer
        :param text: text for user input.
        :return dictionary of arguments.
        """
        value, arguments = self.sinput(text, restricted=False)
        arguments['answer'] = value
        return arguments

# def make_deck(save_location, name, update=False, direct_tuple_input=None):
#     """CLI for deck creation and update
#     :param save_location: where the deck will be saved i.e. home/grindy/decks
#     :param name: name of the deck
#     :param direct_tuple_input: instead of direct input take this as input where list_of_tuples is [(question, answer),...]
#     """
#     questions = []
#     name = name + '.json' if not name.endswith('.json') else name
#     save_path = os.path.join(save_location, name)
#     if update:
#         deck = Deck(save_path)
#         questions = deck.questions
#
#     # Input either from argument
#     if direct_tuple_input:
#         for q in direct_tuple_input:
#             questions.append(Question(question=q[0], answer=q[1]))
#     # Or direct input
#     else:
#         try:
#             while True:
#                 input_question = input(utils.color_text('{} Q: '.format(len(questions) + 1),
#                                                         back=Back.WHITE, color=Fore.BLACK)).strip()
#                 # checking for duplicates
#                 if input_question.lower() in (q.question.lower() for q in questions):
#                     while True:
#                         dup_answer = input('Question already exists, do you want to (c)ancel/(a)dd/(o)verride?').lower()
#                         if dup_answer in ['c', 'a', 'o']:
#                             break
#                     if dup_answer == 'c':
#                         continue
#                     if dup_answer == 'o':
#                         questions = [q for q in questions if q.question != input_question]
#                 input_kwargs = md_sinput(input('{} A: '.format(len(questions) + 1)), questions)
#                 input_kwargs['question'] = input_question
#                 questions.append(Question(input_kwargs))
#         except (KeyboardInterrupt, EOFError):
#             pass
#
#     deck = Deck(save_path, questions)
#     deck.save_deck()
#
#     print('\nDeck "{}" has been saved!'.format(name.replace('.json', '')))
#
#
# def md_sinput(text, questions):
#     """reads user input for arguments
#     :param text: user input.
#     :return dictionary of arguments.
#     """
#     found_arguments = re.findall('\B-+([^\b|^\s]+)([^-]+)', text)
#     arguments = {k: v.strip() for k, v in found_arguments}
#     if 'all_q' in arguments:
#         for q in questions:
#             print(q.question)
#     arguments['answer'] = re.split('|'.join(['-' + arg for arg, value in found_arguments]), text)[0]
#     return arguments
