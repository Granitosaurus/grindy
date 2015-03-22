from colorama import Fore

INPUT_RATINGS = {'1': 90, '2': 50, '3': 10}
RATINGS = {'correct':
               {'match_func': lambda x: x == 100,
                'result_text': 'Correct!',
                'value': 50,
                'color': Fore.GREEN},
           'partial_high':
               {'match_func': lambda x: 100 > x > 80,
                'result_text': 'Almost!',
                'value': 35,
                'color': Fore.YELLOW},
           'partial_low':
               {'match_func': lambda x: 80 > x > 60,
                'result_text': 'Close!',
                'value': 25,
                'color': Fore.YELLOW},
           'incorrect':
               {'match_func': lambda x: 60 > x,
                'result_text': 'Incorrect!',
                'value': 10,
                'color': Fore.RED},
           }
TIMES = {
    'NEW': {
        'count': 0,
        'divider': 10,
    },
    'EASY': {
        'count': 3,   # answered at least 3 times = easy
        'divider': 8  # divides rating addition by value
    },
    'MEDIUM': {
        'count': 5,
        'divider': 5
    },
    'HARD': {
        'count': 10,
        'divider': 3
    },
}
STREAKS = [
    {
        'streak': 1,
        'multiplier': 1.2,
    },
    {
        'streak': 3,
        'multiplier': 1.4,
    },
    {
        'streak': 5,
        'multiplier': 2,
    },
]
MINUS_RATING_PER_HOUR = [(lambda x: x > 24,
                          2),     # threshold to hours to rating_per_hour
                         (lambda x: 24 > x > 12,
                          1.5),
                         (lambda x: 12 > x,
                          1)]
MIN_REDUCE = 10
MAX_REDUCE = 60
HINT_COVERAGE = 30