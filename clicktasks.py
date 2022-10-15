#!/usr/bin/env python3

"""
Show pending tasks.
"""

from datetime import datetime
from urllib.error import HTTPError
from configparser import ParsingError

import cache
from colors import black, red, green, yellow, blue, magenta, cyan, white

status_ignored = ['done (to be reviewed)', 'to test', 'ready', 'blocked']


def main():
    try:
        refresh_url = ('https://api.clickup.com/api/v2'
                       '/team/{team}/task?assignees[]={user}')

        tasks_all = cache.get_data('tasks.json', refresh_url)['tasks']

        tasks = [task for task in tasks_all
                 if task['status']['status'] not in status_ignored]
        tasks.sort(key=lambda x: x['date_created'])  # sort by created date

        for i, task in enumerate(tasks):
            print(f'\n# {i+1} {info(task)}')

        while True:
            i = int(input('\n> ')) - 1
            if not 0 <= i < len(tasks):
                break

            task = tasks[i]
            print(f'\n# {i+1} {info(task)}\n')
            print(green(task['text_content'] or '<no content>'))

    except HTTPError as e:
        print(e)
        print('Maybe there is a problem with your token?')
    except KeyError as e:
        print('Missing key in clickdown.cfg:', e)
    except (FileNotFoundError, ParsingError) as e:
        print(e)
    except (KeyboardInterrupt, EOFError, ValueError) as e:
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
