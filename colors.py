import sys
from collections import namedtuple

Colors = namedtuple('Colors', 'status section priority due url title text')


def ansi(n, bold=False):
    "Return function that escapes text with ANSI color n"
    if sys.stdout.isatty():
        return lambda txt: f'\x1b[{n}{";1" if bold else ""}m{txt}\x1b[0m'
    else:
        return lambda txt: txt

black, red, green, yellow, blue, magenta, cyan, white = map(ansi, range(30, 38))
blackB, redB, greenB, yellowB, blueB, magentaB, cyanB, whiteB = [
    ansi(i, bold=True) for i in range(30, 38)]


def get_colors(theme):
    assert theme in ['light', 'dark', 'none'], 'Unknown theme: %s' % theme

    if theme == 'light':
        return Colors(status=cyan, section=yellow, priority=redB, due=magentaB,
                      url=white, title=blue, text=black)
    elif theme == 'dark':
        return Colors(status=blue, section=magenta, priority=red, due=cyan,
                      url=black, title=yellowB, text=green)
    elif theme == 'none':
        none = lambda x: x
        return Colors(status=none, section=none, priority=none, due=none,
                      url=none, title=none, text=none)
