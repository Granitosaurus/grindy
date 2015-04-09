from datetime import datetime
import json
import os
from urllib import request
from logging import log, ERROR
import re
from urllib.parse import urljoin


class Deck:
    """
    Storage for Deck item
    """
    def __init__(self, loc, questions=None, reverse=False):
        self.reverse = reverse
        self.loc = loc
        self.name = os.path.split(loc)[-1]
        self.questions = questions or []
        if not questions:
            self.read_questions()

    def read_questions(self):
        """reads deck file and creates questions and stores them in self"""
        with open(self.loc, 'r') as deck_file:
            data = json.loads(deck_file.read())
            for question in data['questions']:
                self.questions.append(Question(json_item=question, reverse=self.reverse))

    def save_deck(self):
        """saves current deck object into a .json deck file"""
        with open(self.loc, 'w') as deck_file:
            data = {'questions': [q.__dict__(self.reverse) for q in self.questions]}
            data = json.dumps(data, indent=4, sort_keys=True)
            deck_file.write(data)

    def __iter__(self):
        for question in self.questions:
            yield question

    def __getitem__(self, index):
        return self.questions[index]

    def __len__(self):
        return len(self.questions)


def download_deck(url, name, save_loc):
    """
    Downloads deck from external url (must point directly to .json file)
    :param url: direct url to deck json file
    :param name: name of the deck
    :param save_loc: where to save the deck
    """
    if not name.endswith('.json'):
        name += '.json'
    location = os.path.join(save_loc, name)
    if os.path.isfile(location):
            prompt = input('Deck "{}" already exists in "{}"(y/n)'.format(name, location))
            if True if 'n' in prompt.lower() else False:
                return
    try:
        print('Downloading deck from "{}"'.format(url))
        data = request.urlopen(url).read().decode()
    except ValueError:
        log(ERROR, 'url "{}" is not valid'.format(url))
        return
    try:
        print('Validating deck')
        json_data = json.loads(data)
    except ValueError:
        log(ERROR, 'Failed to validate downloaded deck, aborting.')
        return
    with open(os.path.join(save_loc, name), 'w') as file:
        file.write(json.dumps(json_data, indent=4, sort_keys=True))
        print('File was downloaded and saved to "{}"'.format(os.path.join(save_loc, name)))


def deck_repo(url):
    """
    Traverses git repo files for potential decks
    :param url: url to a public github repository
    """
    response = request.urlopen(url).read().decode()
    files = re.findall('a .+title=\".*?\>', response)
    files = [f for f in files if re.search('\.json', f)]
    for i, file in enumerate(files):
        href = urljoin('http://github.com', ''.join(re.findall('href="(.*?)"', file)))
        name = ''.join(re.findall('title="(.*?)"', file))
        files[i] = (name.replace('.json', ''), href.replace('blob', 'raw'))
    return files


class Question:
    """
    Storage for Question item
    """
    date_format = '%Y-%m-%d %H:%M:%S'
    rating = ''

    def __init__(self, json_item=None, reverse=False, **kwargs):
        arg_container = json_item if json_item else kwargs
        self.reverse = reverse
        if reverse:
            self.answer = arg_container.get('question', '') or arg_container.get('a', '')
            self.question = arg_container.get('answer', '') or arg_container.get('q', '')
        else:
            self.answer = arg_container.get('answer', '') or arg_container.get('a', '')
            self.question = arg_container.get('question', '') or arg_container.get('q', '')
        self.hint = arg_container.get('hint', '') or arg_container.get('h', '')
        self._rating = int(arg_container.get('rating', '0') or '0') or int(arg_container.get('r', '0'))
        self.streak = int(arg_container.get('streak', '0') or '0') or int(arg_container.get('s', '0'))
        self.times = int(arg_container.get('times', '0') or '0') or int(arg_container.get('t', '0'))
        self.last_run = datetime.strptime(arg_container.get('last_run', None)
                                          or datetime.now().strftime(self.date_format), self.date_format)

    @property
    def rating(self):
        return self._rating
    @rating.setter
    def rating(self, value):
        value = 100 if value > 100 else value
        value = 0 if value < 0 else value
        self._rating = value

    def reset(self):
        """resets question progress"""
        self.rating = 0
        self.streak = 0
        self.times = 0
        self.last_run = datetime.now()

    def __dict__(self, reverse=False):
        data = {
            'hint': self.hint,
            'rating': str(self.rating),
            'streak': str(self.streak),
            'times': str(self.times),
            'last_run': self.last_run.strftime(self.date_format),
        }
        if reverse:
            data['question'] = self.answer
            data['answer'] = self.question
        else:
            data['question'] = self.question
            data['answer'] = self.answer
        return data

    def __str__(self):
        return repr(self.__dict__())
