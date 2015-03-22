import os
import argparse
import sys
from colorama import Fore
from grindy import decks
from grindy.grindy import Grindy
from grindy.tools.make_deck import make_deck
from grindy.utils import LINE, print_color


class GrindyArgparser:
    """Argparser for main Grindy application"""
    def __init__(self):
        self.decks = self.find_decks()
        self.decks.sort()
        self.parser = argparse.ArgumentParser(description='Personal Log Book')
        self.setup_parser()
        
    def setup_parser(self):
        """
        Main running function which executes the whole sequence with arguments by using 'argparse' module.
        """
        self.parser.add_argument('-o', '--open', help='open deck <deckname>[.json]')
        self.parser.add_argument('-l', '--list', help='list decks', action='store_true')
        self.parser.add_argument('-md', '--make_deck', help='make a deck')
        self.parser.add_argument('-cs', '--case_sensitive', help='set case sentivity on for q&a', action='store_true',
                                 default=False)
        self.parser.add_argument('-nah', '--no_auto_hints', help='disable auto hints', action='store_true',
                                 default=False)

        args = self.parser.parse_args()

        if args.list:
            print('Decks found:\n{}'.format(LINE))
            self.list_decks()
        if args.make_deck:
            make_deck(args.make_deck)
        if args.open:
            args.open = args.open.replace('.json', '')
            deck_location = self.get_deck_location(args.open)
            if deck_location:
                print_color('Opening deck "{}":\n{}'.format(args.open, LINE), color=Fore.CYAN)
                grindy = Grindy(deck_loc=deck_location,
                                auto_hints=not args.no_auto_hints,
                                ignore_case=not args.case_sensitive)
                grindy.run_deck()
            else:
                sys.exit('Deck "{}" not found, see --list for the decks available'.format(args.open))

    @staticmethod
    def find_decks():
        cwd = os.path.dirname(decks.__file__)
        found_decks = []
        files = os.listdir(cwd)
        found_decks.extend((file.replace('.json', ''), os.path.join(cwd, file))
                           for file in files if file.endswith('.json'))
        return found_decks

    def list_decks(self):
        for deck, location in self.decks:
            print('- {}'.format(deck))

    def get_deck_location(self, deck_name):
        for deck, location in self.decks:
            if deck_name.lower() == deck.lower():
                return location

if __name__ == '__main__':
    GrindyArgparser()
