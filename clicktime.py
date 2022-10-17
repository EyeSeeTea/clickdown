#!/usr/bin/env python3

"""
Show the tracked time in clickup.
"""

from datetime import datetime
from itertools import groupby
from urllib.error import HTTPError
from configparser import ParsingError

import cache
from colors import black, red, green, yellow, blue, magenta, cyan, white


def main():
    try:
        refresh_url = ('https://api.clickup.com/api/v2'
                       '/team/{team}/time_entries')

        entries_all = cache.get_data('time.json', refresh_url)['data']

        entries_all.sort(key=lambda x: x['start'])  # sort by starting date

        for week, group_week in groupby(entries_all, get_week):
            entries_week = list(group_week)  # don't exhaust the iterator

            for day, group_day in groupby(entries_week, get_day):
                entries_day = list(group_day)  # don't exhaust the iterator
                total_day_s = sum(get_duration(entry) for entry in entries_day)

                print('\n== %s (total: %.2f h) ==' % (day, total_day_s / 3600))
                for entry in entries_day:
                    print('\n' + info(entry))

            total_week_s = sum(get_duration(entry) for entry in entries_week)
            print('\n-- (week total: %.2f h) --\n' % (total_week_s / 3600))

    except HTTPError as e:
        print(e)
        print('Maybe there is a problem with your token?')
    except KeyError as e:
        print('Missing key in clickdown.cfg:', e)
    except (FileNotFoundError, ParsingError, ValueError) as e:
        print(e)
    except (KeyboardInterrupt, EOFError) as e:
        pass


def get_week(entry):
    start_s, _ = get_span(entry)
    return datetime.fromtimestamp(start_s).strftime('%U')  # week of the year


def get_day(entry):
    start_s, _ = get_span(entry)
    return datetime.fromtimestamp(start_s).strftime('%a %d %b')  # ~ Tue 04 Oct


def get_duration(entry):
    start_s, end_s = get_span(entry)
    return end_s - start_s


def info(entry):
    "Return a string with information about the entry"
    start_s, end_s = get_span(entry)

    start = datetime.fromtimestamp(start_s).strftime('%H:%M')  # time as HH:MM
    end = datetime.fromtimestamp(end_s).strftime('%H:%M')
    duration = '%.2f h' % ((end_s - start_s) / 3600)
    url = entry['task_url']
    task = entry['task']['name']
    description = entry['description'] or '<empty description>'

    return (f'{start} - {end} ({duration}) {black(url)}\n'
            f'{yellow(task)}\n'
            f'{green(description)}')


def get_span(entry):
    to_s = lambda key: int(entry[key]) // 1000  # seconds since 1970-01-01
    return to_s('start'), to_s('end')



if __name__ == '__main__':
    main()
