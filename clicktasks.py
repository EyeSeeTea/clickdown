#!/usr/bin/env python3

"""
Show pending tasks.
"""

import sys
from datetime import datetime
from configparser import ConfigParser, ParsingError
from urllib.error import HTTPError
import readline

import cache
from colors import get_colors


def main():
    try:
        cfg = read_config()

        refresh_url = ('https://api.clickup.com/api/v2'
                       '/team/{team}/task?assignees[]={user}')

        tasks_all = cache.get_data('tasks.json', refresh_url, cfg)['tasks']

        ignored = cfg.get('ignored', '').split(',')
        tasks = [task for task in tasks_all
                 if task['status']['status'] not in ignored]
        tasks.sort(key=lambda x: x['date_created'])  # sort by created date

        colors = get_colors(cfg.get('theme', 'dark'))

        for i, task in enumerate(tasks):
            print(f'\n# {i+1} ' + info(task, colors))

        if not sys.stdout.isatty():
            sys.exit()  # skip interactive mode if redirecting the output

        task_names = [task['name'] for task in tasks]
        readline_init(task_names)

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

    except HTTPError as e:
        print(e)
        sys.exit('Maybe there is a problem with your token?')
    except KeyError as e:
        sys.exit('Missing key in clickdown.cfg:', e)
    except (FileNotFoundError, ParsingError, ValueError, AssertionError) as e:
        sys.exit(e)
    except (KeyboardInterrupt, EOFError) as e:
        print()
        sys.exit()


def read_config():
    cp = ConfigParser()
    with open('clickdown.cfg') as fp:
        cp.read_string('[top]\n' + fp.read())
    return cp['top']


def readline_init(names):
    "Initialize readline using the given names to complete"
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set show-all-if-ambiguous on')

    readline.set_completer_delims('')  # use full sentence, not just words

    def completer(text, state):
        matches = [name for name in names if text.lower() in name.lower()]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)


def info(task, colors):
    "Return a string with information about the task"
    status = colors.status(task['status']['status'])
    lname = colors.section(task['list']['name'])
    name = colors.title(task['name'])
    url = colors.url(task['url'])

    priority = colors.priority((('priority %s ' % task['priority']['priority'])
                                if task['priority'] else ''))
    due_date = colors.due(('due %s ' % to_date(task['due_date'])
                           if task['due_date'] else ''))

    return (f'{name}\n'
            f'{lname} - {status} - {priority}{due_date}{url}')



def to_date(str_ms):
    return datetime.fromtimestamp(int(str_ms) // 1000).strftime('%a %d %b')



if __name__ == '__main__':
    main()
