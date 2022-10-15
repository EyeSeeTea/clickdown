#!/usr/bin/env python3

"""
Show the tracked time in clickup.
"""

from datetime import datetime
from itertools import groupby
from urllib.error import HTTPError

import cache
from colors import black, red, green, yellow, blue, magenta, cyan, white


def main():
    try:
        team = 4528615  # the id of the EyeSeeTea team
        refresh_endpoint = f'/team/{team}/time_entries'

        entries_all = cache.get_data('time.json', refresh_endpoint)['data']

        entries_all.sort(key=lambda x: x['start'])  # sort by starting date

        for day, group in groupby(entries_all, get_day):
            entries = list(group)  # so we don't exhaust the iterator
            total_s = sum(get_duration(entry) for entry in entries)

            print('\n== %s (total: %.2f h) ==' % (day, total_s / 3600))
            for entry in entries:
                print('\n' + info(entry))

    except FileNotFoundError as e:
        print(e)
    except HTTPError as e:
        print(e)
        print('Maybe there is a problem with your token?')


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
