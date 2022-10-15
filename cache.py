"""
Cached queries.
"""

import os
import time
import json
from urllib.request import Request, urlopen

urlbase = 'https://api.clickup.com/api/v2'

cdir = os.environ.get('XDG_CACHE_HOME',
                      f'{os.environ["HOME"]}/.cache') + '/clickdown'


def get_data(fname, refresh_endpoint):
    "Return data as they come from an api request"
    fp, age = read(fname)

    if fp:
        if age < 3600:
            print(f'Reading from {cdir}/{fname} ...')
            return json.loads(fp.read())
        else:
            print('Cache file is too old and will update.')
            fp.close()

    token = open('token.txt').read().strip()
    url = f'{urlbase}{refresh_endpoint}'
    req = Request(url, headers={'Authorization': token})

    print(f'Connecting to {url} ...')
    data = urlopen(req).read()

    print(f'Caching result for the next hour to {cdir}/{fname} ...')
    write(fname, data)

    return json.loads(data)


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
