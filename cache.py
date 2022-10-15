import os
import time

cdir = os.environ.get('XDG_CACHE_HOME',
                      f'{os.environ["HOME"]}/.cache') + '/clickdown'


def read(fname):
    "Return the file pointer and age of the cache file if it exists"
    cache = f'{cdir}/{fname}'

    if not os.path.exists(cache):
        return None, None

    return open(cache), time.time() - os.stat(cache).st_mtime


def write(fname, data):
    if not os.path.exists(cdir):
        os.mkdir(cdir)

    cache = f'{cdir}/{fname}'
    open(cache, 'wb').write(data)
