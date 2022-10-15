"""
Cached queries.
"""

import os
import time
import json
from urllib.request import Request, urlopen

urlbase = 'https://api.clickup.com/api/v2'

cachedir = os.environ.get('XDG_CACHE_HOME',
                          f'{os.environ["HOME"]}/.cache') + '/clickdown'
configdir = os.environ.get('XDG_CONFIG_HOME',
                           f'{os.environ["HOME"]}/.config') + '/clickdown'

def get_data(fname, refresh_endpoint):
    "Return data as they come from an api request"
    fp, age = read(fname)

    if fp:
        if age < 3600:
            print(f'Reading from {cachedir}/{fname} ...')
            return json.loads(fp.read())
        else:
            print('Cache file is too old and will update.')
            fp.close()

    token = get_token()

    url = f'{urlbase}{refresh_endpoint}'
    req = Request(url, headers={'Authorization': token})

    print(f'Connecting to {url} ...')
    data = urlopen(req).read()

    print(f'Caching result for the next hour to {cachedir}/{fname} ...')
    write(fname, data)

    return json.loads(data)


def read(fname):
    "Return the file pointer and age of the cache file if it exists"
    cache = f'{cachedir}/{fname}'

    if not os.path.exists(cache):
        return None, None

    return open(cache), time.time() - os.stat(cache).st_mtime


def write(fname, data):
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    cache = f'{cachedir}/{fname}'
    open(cache, 'wb').write(data)


def get_token():
    if os.path.exists('token.txt'):
        print('Reading token from local file token.txt ...')
        return open('token.txt').read().strip()
    elif os.path.exists(f'{configdir}/token.txt'):
        print(f'Reading token from {configdir}/token.txt ...')
        return open(f'{configdir}/token.txt').read().strip()
    else:
        print('Token not found. Input token below and/or see readme.md.')
        return input('Token: ').strip()
