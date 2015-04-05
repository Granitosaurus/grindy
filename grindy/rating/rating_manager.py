from rating.ratting_settings import *


def reduce_rating_by_time(current_rating, gap_hours):
    """Reduces rating according to the time gap between last run and the new one"""
    for threshold, rating_per_hour in MINUS_RATING_PER_HOUR:
        if not threshold(gap_hours):
            continue
        reduction = round(gap_hours * rating_per_hour)
        if reduction < MIN_REDUCE:  # threshold not met return original
            return current_rating
        reduction = MAX_REDUCE if reduction > MAX_REDUCE else reduction

        reduced_rating = current_rating - reduction
        reduced_rating = 0 if reduced_rating < 0 else reduced_rating
        return reduced_rating


def rate(question, rating, value=None):
    """
    rates question
    :param question: question object to rate
    :param rating: rating value which must comply with INPUT_RATINGS from rating_settings
    """
    rating = str(rating)
    if not value:
        if rating not in RATINGS and rating not in INPUT_RATINGS:
            raise NotImplementedError('rating {} not found in RATINGS dict'.format(rating))
        try:
            value = RATINGS[rating]['value']
        except KeyError:
            value = INPUT_RATINGS[rating]['value']

    def get_highest_time(times):
        highest = TIMES['NEW']
        for t in TIMES:
            if times >= TIMES[t]['count'] > highest['count']:
                highest = TIMES[t]
        return highest
    divider = get_highest_time(question.times)['divider']
    multiplier = 1
    for streak in STREAKS:
        if question.streak > streak['streak'] and streak['multiplier'] > multiplier:
            multiplier = streak['multiplier']
    question.rating += int(value / divider * multiplier)
    if question.rating > 100:
        question.rating = 100