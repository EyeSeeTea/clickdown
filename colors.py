import sys

def ansi(n):
    "Return function that escapes text with ANSI color n"
    if sys.stdout.isatty():
        return lambda txt: '\x1b[%dm%s\x1b[0m' % (n, txt)
    else:
        return lambda txt: txt

black, red, green, yellow, blue, magenta, cyan, white = map(ansi, range(30, 38))
