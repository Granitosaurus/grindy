from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime
import time
import random
from colorama import Back

from grindy.deck import Deck

# Output helpers
from grindy.input_manager import sinput
from grindy.rating.rating_manager import rate, reduce_rating_by_time
from grindy.rating.rating_settings import RATINGS
from grindy.utils import print_color


class Grindy():
    def __init__(self, deck_loc=None, **kwargs):
        self.deck_loc = deck_loc or "decks/alphabet.json"
        self.deck = None
        self.stats = {'total_rating': 0,
                      'total_answers': 0,
                      'highest_streak': 0,
                      'total_time': None,
                      'answers': Counter()}
        self.ignore_case = kwargs.get('ignore_case', True)
        self.auto_hints = kwargs.get('auto_hints', True)

    def run_deck(self):
        self.open_deck(self.deck_loc)
        random.shuffle(self.deck.questions)
        old_deck = Deck(self.deck.loc)
        start_time = datetime.now()
        answered = []
        try:
            # for question in self.deck.questions:
            previous_question = None
            while True:
                questions_left = len([q for q in self.deck.questions if q.rating < 100])
                if questions_left == 1:  # only 1 question below 100 rating
                    question = self.weighted_choice()
                    print('Last Question left! You should take a break, increase difficulty or reset the deck :)')
                elif questions_left == 0:
                    print('Deck is completed! ratings drop over time so come back tomorrow! '
                          'or reset the deck via "grindy --reset_deck <deck_name>"')
                    raise KeyboardInterrupt
                else:
                    question = self.weighted_choice()
                    if previous_question:
                        if previous_question.question is question.question:
                            continue
                # Actual interaction
                print_color('Q: {}'.format(question.question), back=Back.BLUE)
                answer = sinput('A: ', question=question, grindy=self)
                self.check_answer(answer, question)

                previous_question = question
                answered.append(question)
        except (KeyboardInterrupt, EOFError):
            self.deck.save_deck()
            quit_text = 'STOPPED AND SAVING'
            print()
            print_color(quit_text, back=Back.RED)

            # Stats
            self.stats['total_time'] = (datetime.now() - start_time).seconds
            self.stats['answers'] = dict(self.stats['answers'])
            self.calculate_stats(old_deck)
            print('stats:', repr(self.stats))

    def check_answer(self, answer, question):
        """
        Checks question partially and asserts rating
        :param answer: input answer
        :param question: question object
        """
        old_rating = question.rating
        gap = (datetime.now() - question.last_run).seconds
        question.last_run = datetime.now()
        question.times += 1
        question.rating = reduce_rating_by_time(question.rating, gap / 3600)
        reduced_rating = question.rating

        sm = SequenceMatcher()
        sm.set_seq1(answer.lower() if self.ignore_case else answer)
        sm.set_seq2(question.answer.lower() if self.ignore_case else question.answer)
        match = sm.ratio() * 100

        if match == 100:
            question.streak += 1
            if question.streak > self.stats['highest_streak']:
                self.stats['highest_streak'] = question.streak

        for rating, data in RATINGS.items():
            if data['match_func'](match):
                rate(question, rating)
                self.stats['answers'][rating] += 1
                if reduced_rating != old_rating:
                    ratio_progress = '{}->{}->{}'.format(old_rating, reduced_rating, question.rating)
                else:
                    ratio_progress = '{}->{}'.format(old_rating, question.rating)
                text = '{}{} ({})'.format(data['result_text'],
                                          ' A: ' + question.answer if match != 100 else '',
                                          ratio_progress)
                print_color(text, data['color'])
                break

    def open_deck(self, deck_location):
        """
        Opens a deck file from a category
        :param deck_location: deck location
        """
        if not deck_location.endswith('.json'):
            deck_location += '.json'
        self.deck = Deck(deck_location)

    def weighted_choice(self):
        total = sum(100 - q.rating for q in self.deck.questions)
        r = random.uniform(0, total)
        upto = 0

        for question in self.deck.questions:
            weight = (100 - question.rating)
            if upto + weight > r:
                return question
            upto += (100 - question.rating)
        # if all questions are at 100 rating return random one
        return random.choice(self.deck.questions)

    def calculate_stats(self, old_deck):
        """
        Calculates and populates self.stats using current state of deck and state of the deck in the beginning
        """
        new_deck = self.deck
        for index in range(len(new_deck)):
            self.stats['total_rating'] += new_deck[index].rating - old_deck[index].rating
            self.stats['total_answers'] += new_deck[index].times - old_deck[index].times

        # Total time
        if self.stats['total_time'] > 3600:
            self.stats['total_time'] = time.strftime('%H:%M:%S', time.gmtime(self.stats['total_time']))
        else:
            self.stats['total_time'] = time.strftime('%M:%S', time.gmtime(self.stats['total_time']))
