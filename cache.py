"""
Cached queries.
"""

import os
import time
import json
from urllib.request import Request, urlopen

cachedir = os.environ.get('XDG_CACHE_HOME',
                          f'{os.environ["HOME"]}/.cache') + '/clickdown'


def get_data(fname, refresh_url, cfg):
    "Return data as they come from an api request"
    fp, age = read_cache(fname)

    if fp:
        if age < int(cfg.get('cache_age_max', 3600)):  # in seconds
            print(f'Reading from {cachedir}/{fname} ...')
            return json.loads(fp.read())
        else:
            print('Cache file is too old and will update.')
            fp.close()

    url = refresh_url.format(team=cfg['team'], user=cfg.get('user', '0000'))
    req = Request(url, headers={'Authorization': cfg['token']})

    print(f'Connecting to {url} ...')
    data = urlopen(req).read()

    print(f'Caching result for the next hour in {cachedir}/{fname} ...')
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

    cache = f'{cachedir}/{fname}'
    open(cache, 'wb').write(data)
