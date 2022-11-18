"""
Cached queries.
"""

import os
import time
import json
from urllib.request import Request, urlopen

cachedir = os.environ.get('XDG_CACHE_HOME',
                          f'{os.environ["HOME"]}/.cache') + '/clickdown'


def retrieve(fname, url, cfg):
    "Read data from cache or url, return it and cache it"
    fp, age = read_cache(fname)

    if not cfg['refresh'] and fp is not None:
        if age < int(cfg.get('cache_age_max', 3600)):  # in seconds
            print(f'Reading from {cachedir}/{fname} ...')
            return json.loads(fp.read())
        else:
            print('Cache file is too old and will update.')
            fp.close()

    url_full = url.format(team=cfg['team'], user=cfg.get('user', '0000'))
    req = Request(url_full, headers={'Authorization': cfg['token']})

    print(f'Connecting to {url_full} ...')
    data = urlopen(req).read()

    print(f'Caching result in {cachedir}/{fname} ...')
    write_cache(fname, data)

    return json.loads(data)


def read_cache(fname):
    "Return the file pointer and age of the cache file if it exists"
    cache = f'{cachedir}/{fname}'

    if not os.path.exists(cache):
        return None, None

    return open(cache), time.time() - os.stat(cache).st_mtime


def write_cache(fname, data):
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    with open(f'{cachedir}/{fname}', 'wb') as fp:
        fp.write(data)
