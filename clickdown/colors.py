import sys
from collections import namedtuple

Colors = namedtuple('Colors', 'status section priority due url title text')


def ansi(n, bold=False):
    "Return function that escapes text with ANSI color n"
    return lambda txt: f'\x1b[{n}{";1" if bold else ""}m{txt}\x1b[0m'

none = lambda txt: txt  # function that doesn't colorize its input text
black, red, green, yellow, blue, magenta, cyan, white = [
    ansi(i) for i in range(30, 38)]  # some colors (non-bold version)
blackB, redB, greenB, yellowB, blueB, magentaB, cyanB, whiteB = [
    ansi(i, bold=True) for i in range(30, 38)]  # bold version of the colors


def get_colors(theme):
    assert theme in ['none', 'light', 'dark'], 'Unknown theme: %s' % theme

    if theme == 'none' or not sys.stdout.isatty():
        return Colors(status=none, section=none, priority=none, due=none,
                      url=none, title=none, text=none)
    elif theme == 'light':
        return Colors(status=cyan, section=yellow, priority=redB, due=magentaB,
                      url=white, title=blue, text=black)
    elif theme == 'dark':
        return Colors(status=blue, section=magenta, priority=red, due=cyan,
                      url=black, title=yellowB, text=green)
