import logging
import os
import argparse
import sys
from colorama import Back
import shutil
from grindy.deck import Deck, download_deck, deck_repo
from grindy.grindy import Grindy
from grindy.settings import repo_urls
from grindy.tools.make_deck import make_deck
from grindy.utils import LINE, print_color


class GrindyArgparser:
    """Argparser for main Grindy application"""
    name = 'grindy'
    default_location = os.path.join(os.path.expanduser("~"), name)

    def __init__(self):
        self.location = ''
        self.deck_location = ''
        self.decks = []
        self.parser = argparse.ArgumentParser(description='Long term memory training console application.')
        self.setup_parser()
        
    def setup_parser(self):
        """
        Main running function which executes the whole sequence with arguments by using 'argparse' module.
        """
        self.parser.add_argument('-o', '--open', help='open deck <deckname>[.json]', metavar='DECK')
        self.parser.add_argument('-l', '--list', help='list decks', action='store_true')
        self.parser.add_argument('-dl', '--download', help='download deck from direct url',
                                 metavar='NAME URL', nargs='*')
        self.parser.add_argument('-rl', '--repo_list', help='list decks in the deck repos', action='store_true')
        self.parser.add_argument('-rdl', '--repo_download', help='Download a deck from repo', metavar='DECK')
        self.parser.add_argument('-md', '--make_deck', help='make a deck', metavar='NAME')
        self.parser.add_argument('-del', help='delete deck', metavar='DECK')
        self.parser.add_argument('--reset_deck', help='reset deck of any progress', metavar='DECK')
        self.parser.add_argument('-init', help='setup grindy in provided location '
                                               '(no location uses current working directory)', action='store_true')
        self.parser.add_argument('-loc', '--deck_location', help='decks location', action='store_true')
        self.parser.add_argument('-cs', '--case_sensitive', help='set case sentivity on for q&a', action='store_true',
                                 default=False)
        self.parser.add_argument('-nah', '--no_auto_hints', help='disable auto hints', action='store_true',
                                 default=False)

        args = self.parser.parse_args()
        if len(sys.argv) <= 1:
            self.parser.print_usage()
            return

        if args.deck_location:
            self.location = args.deck_location
        else:
            self.location = self.default_location
        self.deck_location = os.path.join(self.location, 'decks')

        if args.download:
            name = args.download[0]
            url = args.download[1]
            download_deck(url, name, self.deck_location)

        if args.repo_download:
            decks = []
            for url in repo_urls:
                decks.extend(deck_repo(url))
            for index, deck in enumerate(decks):
                if args.repo_download == deck[0] or str(args.repo_download) == str(index):
                    download_deck(deck[1], deck[0], self.deck_location)
                    return
                print('No decks of name or #id of "{}" found'.format(args.repo_download))

        if args.repo_list:
            decks = []
            for url in repo_urls:
                decks.extend(deck_repo(url))
            row = lambda i, name, url: ('|' + '| '.join([i.ljust(5), name.ljust(45), url.ljust(25)])) + '|'
            print('_'*80)
            print(row('index', 'Name', 'Url'))
            print('_'*80)
            for index, deck in enumerate(decks):
                print(row(str(index), deck[0], deck[1]))

        if args.init:
            self.initiate_grindy()
            return
        self.decks = self.find_decks()

        if args.list:
            print('Decks found:\n{}'.format(LINE))
            self.list_decks()
        if getattr(args, 'del'):
            if 'y' in input('Are you sure?(y/n) ').lower():
                self.remove_deck(self.deck_location, getattr(args, 'del'))
        if args.reset_deck:
            if 'y' in input('Are you sure?(y/n) ').lower():
                print('Resetting deck "{}"'.format(args.reset_deck))
                self.reset_deck(self.deck_location, args.reset_deck)

        if args.make_deck:
            make_deck(self.deck_location, args.make_deck)
        if args.open:
            args.open = args.open.replace('.json', '')
            deck_location = self.get_deck_location(args.open)
            if deck_location:
                print_color('Opening deck "{}":'.format(args.open), back=Back.BLUE)
                print_color('_'*80, back=Back.BLUE)
                grindy = Grindy(deck_loc=deck_location,
                                auto_hints=not args.no_auto_hints,
                                ignore_case=not args.case_sensitive)
                grindy.run_deck()
            else:
                sys.exit('Deck "{}" not found, see --list for the decks available'.format(args.open))

    def find_decks(self, location=None):
        """
        Finds decks in provided location
        :param location: path string
        :return: list of tuples (name, path)
        """
        if not location:
            location = self.location
        found_decks = []
        decks_location = os.path.join(location, 'decks')
        try:
            files = os.listdir(decks_location)
        except FileNotFoundError:
            sys.exit('grindy is not set up, use grindy -init to set it up')
        found_decks.extend((file.replace('.json', ''), os.path.join(decks_location, file))
                           for file in files if file.endswith('.json'))
        return found_decks
    
    def initiate_grindy(self):
        """
        initiates grindy into provided --location or default home/grindy
        """
        if not os.path.exists(self.location):
            if input("""Initiate grindy in location: "{}" ? (y/n) """.format(self.location)).lower() == 'y':
                os.makedirs(self.location)
                os.makedirs(os.path.join(self.location, 'decks'))
                for default_deck in self.find_decks(os.path.dirname(__file__)):
                    shutil.copyfile(default_deck[1], os.path.join(self.deck_location, default_deck[0] + '.json'))
                print('Grindy was set up at "{}"!'.format(self.location))
        else:
            print('Grindy already exists at "{}"'.format(self.location))
    
    def list_decks(self):
        """prints decks found in the grindy deck"""
        for deck, location in self.decks:
            print('- {}'.format(deck))

    def get_deck_location(self, deck_name):
        """retrieves location of a deck"""
        for deck, location in self.decks:
            if deck_name.lower() == deck.lower():
                return location

    @staticmethod
    def remove_deck(deck_location, name):
        """Deletes a deck
        :param deck_location: location of grindy decks folder
        :param name: name of the deck
        """
        file_name = name
        if not file_name.endswith('.json'):
            file_name += '.json'
        try:
            os.remove(os.path.join(deck_location, file_name))
        except FileNotFoundError:
            print('deck "{}" does not exist, check "grindy --list" for available decks'.format(name))
        else:
            print('deck "{}" successfully deleted'.format(name))

    @staticmethod
    def reset_deck(deck_location, name):
        """
        Resets deck progress
        :param deck_location: location to grindy decks folder
        :param name: name of the deck
        """
        file_name = name
        if not file_name.endswith('.json'):
            file_name += '.json'
        location = os.path.join(deck_location, file_name)
        try:
            deck = Deck(location)
        except FileNotFoundError:
            print('deck "{}" does not exist, check "grindy --list" for available decks'.format(name))
        else:
            for question in deck:
                question.reset()
            deck.save_deck()
            print('deck "{}" stats were reset'.format(name))


def main():
    """runs the whole CLI and serves as an entry program from 'grindy' command"""
    GrindyArgparser()
