#!/usr/bin/env python3

"""
Show pending tasks.
"""

import sys
from datetime import datetime
from configparser import ParsingError
from urllib.error import HTTPError
import readline

from clickdown import config
from clickdown import cache
from clickdown.colors import get_colors


def main():
    try:
        url = ('https://api.clickup.com/api/v2'
               '/team/{team}/task?assignees[]={user}&subtasks=true')

        cfg = config.init(__doc__)

        tasks_all = cache.retrieve('tasks.json', url, cfg)['tasks']

        tasks = filter_status(tasks_all, cfg.get('ignored'), cfg.get('status'))

        tasks.sort(key=lambda x: x['date_created'])  # sort by created date

        colors = get_colors(cfg.get('theme', 'dark'))

        for i, task in enumerate(tasks):  # print summaries of tasks
            print(f'\n# {i+1} ' + info(task, colors))

        if sys.stdout.isatty():  # skip interactive mode if redirecting output
            interactive_view(tasks, colors)

    except HTTPError as e:
        print(e)
        sys.exit('Maybe there is a problem with your token?')
    except KeyError as e:
        sys.exit('Missing key in %s: %s' % (cfg['config'], e))
    except (FileNotFoundError, ParsingError, ValueError, AssertionError) as e:
        sys.exit(e)
    except (KeyboardInterrupt, EOFError) as e:
        print()
        sys.exit()


def filter_status(tasks, ignored, status):
    if status:
        print(f'Selecting only tasks with status: {status}')
        return [task for task in tasks
                if task['status']['status'] in status.split(',')]
    elif ignored:
        print(f'Selecting tasks except for status: {ignored}')
        return [task for task in tasks
                if task['status']['status'] not in ignored.split(',')]
    else:
        return tasks


def info(task, colors):
    "Return a string with information about the task"
    status = colors.status(task['status']['status'])
    lname = colors.section(task['list']['name'])
    name = colors.title(task['name'])
    url = colors.url(task['url'])

    priority = colors.priority(('priority %s ' % task['priority']['priority'])
                               if task['priority'] else '')
    due_date = colors.due('due %s ' % to_date(task['due_date'])
                          if task['due_date'] else '')

    return (f'{name}\n'
            f'{lname} - {status} - {priority}{due_date}{url}')


def to_date(str_ms):
    "Return a readable recent date from a str with milliseconds since 1970"
    # E.g. 1656558000000 -> 'Thu 30 Jun'
    return datetime.fromtimestamp(int(str_ms) // 1000).strftime('%a %d %b')


def interactive_view(tasks, colors):
    "Ask for a task and show its details"
    task_names = [task['name'] for task in tasks]

    readline_init(task_names)

    print('\nView task details (you can select by number or by name, '
          'use arrows, tab, Ctrl+r, etc.):', end='')

    while True:
        choice = input('\n> ')

        if not choice:
            break
        elif choice.isdecimal():
            i = int(choice) - 1
            assert 0 <= i < len(tasks), f'Unknown task number: {i+1}'
        else:
            i = task_names.index(choice)

        task = tasks[i]
        print(f'\n# {i+1} ' + info(task, colors) + '\n')
        print(colors.text(task['text_content'] or '<no content>'))


def readline_init(names):
    "Initialize readline using the given names to complete"
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set show-all-if-ambiguous on')

    readline.set_completer_delims('')  # use full sentence, not just words
    readline.set_auto_history(False)  # do not add new lines to history

    for name in names:
        readline.add_history(name)  # so one can scroll and search them

    def completer(text, state):
        matches = [name for name in names if text.lower() in name.lower()]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)



if __name__ == '__main__':
    main()
