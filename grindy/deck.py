from datetime import datetime
import json
import os


class Deck:
    """
    Storage for Deck item
    """
    def __init__(self, loc, questions=None):
        self.loc = loc
        self.name = os.path.split(loc)[-1]
        self.questions = questions or []
        if not questions:
            self.read_questions()

    def read_questions(self):
        with open(self.loc, 'r') as deck_file:
            data = json.loads(deck_file.read())
            for question in data['questions']:
                self.questions.append(Question(json_item=question))

    def save_deck(self):
        with open(self.loc, 'w') as deck_file:
            data = {'questions': [q.__dict__() for q in self.questions]}
            data = json.dumps(data)
            deck_file.write(data)

    def __iter__(self):
        for question in self.questions:
            yield question

    def __getitem__(self, index):
        return self.questions[index]

    def __len__(self):
        return len(self.questions)


class Question:
    """
    Storage for Question item
    """
    date_format = '%Y-%m-%d %H:%M:%S'
    rating = ''

    def __init__(self, json_item=None, **kwargs):
        arg_container = json_item if json_item else kwargs

        self.question = arg_container.get('question', '') or arg_container.get('q', '')
        self.hint = arg_container.get('hint', '') or arg_container.get('h', '')
        self.answer = arg_container.get('answer', '') or arg_container.get('a', '')
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
        self.rating = 0
        self.streak = 0
        self.times = 0
        self.last_run = datetime.now()

    def __dict__(self):
        data = {
            'question': self.question,
            'hint': self.hint,
            'answer': self.answer,
            'rating': str(self.rating),
            'streak': str(self.streak),
            'times': str(self.times),
            'last_run': self.last_run.strftime(self.date_format),
        }
        return data

    def __str__(self):
        return repr(self.__dict__())
