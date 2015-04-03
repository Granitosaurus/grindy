from colorama import Fore, Back

LINE = '-'*80


def print_color(*args, **kwargs):
    print(color_text(*args, **kwargs))


def color_text(text, color=Fore.RESET, back=Back.RESET):
    return '{}{}{}{}{}'.format(color, back, text.ljust(80), Fore.RESET, Back.RESET)

if __name__ == '__main__':
    print_color('hello', back=Back.YELLOW)