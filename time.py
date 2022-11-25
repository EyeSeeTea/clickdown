#!/usr/bin/env python3

"""
Show the tracked time in clickup.
"""

import sys
from datetime import datetime
from itertools import groupby
from configparser import ParsingError
from urllib.error import HTTPError

from clickdown import config
from clickdown import cache
from clickdown.colors import get_colors

now = datetime.timestamp(datetime.now())


def main():
    try:
        url = ('https://api.clickup.com/api/v2'
               '/team/{team}/time_entries')

        cfg = config.init(__doc__)

        entries_all = cache.retrieve('time.json', url, cfg)['data']

        days_max = min(float(cfg.get('days_max', 14)), 30)  # the api gives 30
        print('\nShowing entries for the last %g days:' % days_max)

        entries_recent = [entry for entry in entries_all
                          if (now - get_span(entry)[1]) < days_max * 24 * 3600]

        entries_recent.sort(key=lambda x: x['start'])  # sort by starting date

        colors = get_colors(cfg.get('theme', 'dark'))

        for week, group_week in groupby(entries_recent, get_week):
            entries_week = list(group_week)  # don't exhaust the iterator

            for day, group_day in groupby(entries_week, get_day):
                entries_day = list(group_day)  # don't exhaust the iterator
                total_day_s = sum(get_duration(entry) for entry in entries_day)

                print('\n== %s (total: %.1f h) ==' % (day, total_day_s / 3600))
                for entry in entries_day:
                    print('\n' + info(entry, colors))

            total_week_s = sum(get_duration(entry) for entry in entries_week)
            print('\n-- (week total: %.1f h) --\n' % (total_week_s / 3600))

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


def get_week(entry):
    start_s, _ = get_span(entry)
    return datetime.fromtimestamp(start_s).strftime('%U')  # week of the year


def get_day(entry):
    start_s, _ = get_span(entry)
    return datetime.fromtimestamp(start_s).strftime('%a %d %b')  # ~ Tue 04 Oct


def get_duration(entry):
    start_s, end_s = get_span(entry)
    return end_s - start_s


def info(entry, colors):
    "Return a string with information about the entry"
    start_s, end_s = get_span(entry)

    start = datetime.fromtimestamp(start_s).strftime('%H:%M')  # time as HH:MM
    end = datetime.fromtimestamp(end_s).strftime('%H:%M')
    duration = '%.2f h' % ((end_s - start_s) / 3600)
    url = colors.url(entry['task_url'])
    task = colors.title(entry['task']['name'])
    description = colors.text(entry['description'] or '<empty description>')

    return (f'{start} - {end} ({duration}) {url}\n'
            f'{task}\n'
            f'{description}')


def get_span(entry):
    to_s = lambda key: int(entry[key]) // 1000  # seconds since 1970-01-01
    return to_s('start'), to_s('end')



if __name__ == '__main__':
    main()
