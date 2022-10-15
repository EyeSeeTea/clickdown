#!/usr/bin/env python3

"""
See pending tasks.
"""

from datetime import datetime
from urllib.error import HTTPError

import cache
from colors import black, red, green, yellow, blue, magenta, cyan, white

status_ignored = ['done (to be reviewed)', 'to test', 'ready', 'blocked']


def main():
    try:
        team = 4528615  # the id of the EyeSeeTea team
        user = 38428504  # your personal id
        refresh_endpoint = f'/team/{team}/task?assignees[]={user}'

        tasks_all = cache.get_data('tasks.json', refresh_endpoint)['tasks']

        tasks = [task for task in tasks_all
                 if task['status']['status'] not in status_ignored]
        tasks.sort(key=lambda x: x['date_created'])  # sort by created date

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



if __name__ == '__main__':
    main()
