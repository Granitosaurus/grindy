from colorama import Fore, Back

LINE = '-'*80


def print_color(*args, **kwargs):
    """prints color_text()"""
    print(color_text(*args, **kwargs))


def color_text(text, color=Fore.RESET, back=Back.RESET):
    """colors the text"""
    return '{}{}{}{}{}'.format(color, back, text.ljust(80), Fore.RESET, Back.RESET)
