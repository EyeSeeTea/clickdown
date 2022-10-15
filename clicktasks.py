#!/usr/bin/env python3

"""
See pending tasks.
"""

import os
import json
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError


urlbase = 'https://api.clickup.com/api/v2'

status_ignored = ['done (to be reviewed)', 'to test', 'ready', 'blocked']

cache = os.environ.get('XDG_CACHE_HOME',
                       f'{os.environ["HOME"]}/.cache') + '/clickdown/tasks.json'


def main():
    try:
        tasks = [task for task in get_tasks()
                 if task['status']['status'] not in status_ignored]
        tasks.sort(key=lambda x: x['date_created'])

        for i, task in enumerate(tasks):
            print(f'\n# {i+1} {info(task)}')

        while True:
            i = int(input('\n> ')) - 1
            assert 0 <= i < len(tasks)

            task = tasks[i]
            print(f'\n# {i+1} {info(task)}\n')
            print(green(task['text_content'] or '<no content>'))

    except FileNotFoundError as e:
        print(e)
    except HTTPError as e:
        print(e)
        print('Maybe there is a problem with your token?')
    except (KeyboardInterrupt, EOFError, ValueError, AssertionError) as e:
        pass


def get_tasks():
    "Return list of tasks as they come from an api request"
    fp, age = read_cache()

    if fp:
        if age < 3600:
            print(f'Reading from {cache} ...')
            return json.loads(fp.read())['tasks']
        else:
            print('Cache file is too old and will update.')
            fp.close()

    token = open('token.txt').read().strip()
    team = 4528615  # the id of the EyeSeeTea team
    user = 38428504  # your personal id

    url = f'{urlbase}/team/{team}/task?assignees[]={user}'
    req = Request(url, headers={'Authorization': token})

    print(f'Connecting to {urlbase} ...')
    data = urlopen(req).read()

    print(f'Caching result for the next hour to {cache} ...')
    write_cache(data)

    return json.loads(data)['tasks']


def info(task):
    "Return a string with information about the task"
    status = task['status']['status']
    lname = task['list']['name']
    name = task['name']
    url = task['url']

    priority = (('priority %s ' % task['priority']['priority'])
                if task['priority'] else '')
    due_date = ('due %s ' % to_date(task['due_date'])
                if task['due_date'] else '')

    return (f'({blue(status)}) {magenta(lname)} '
            f'{red(priority)}{cyan(due_date)}{black(url)}\n'
            f'{yellow(name)}')


def to_date(str_ms):
    return datetime.fromtimestamp(int(str_ms) // 1000).strftime('%a %d %b')


def read_cache():
    "Return the file pointer and age of the cache file if it exists"
    if not os.path.exists(cache):
        return None, None

    return open(cache), time.time() - os.stat(cache).st_mtime


def write_cache(data):
    cdir = os.path.dirname(cache)
    if not os.path.exists(cdir):
        os.mkdir(cdir)

    open(cache, 'wb').write(data)


def ansi(n):
    "Return function that escapes text with ANSI color n"
    return lambda txt: '\x1b[%dm%s\x1b[0m' % (n, txt)

black, red, green, yellow, blue, magenta, cyan, white = map(ansi, range(30, 38))



if __name__ == '__main__':
    main()
