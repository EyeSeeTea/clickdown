#!/usr/bin/env python3

"""
Show the tracked times in clickup.
"""

# To get the token, go to clickup -> user (bottom left) -> Apps.
# See: https://clickup.com/api/developer-portal/authentication/#personal-token
#
# Reference about the clickup api:
# https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/

from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

urlbase = 'https://api.clickup.com/api/v2'


def main():
    try:
        token = open('token.txt').read().strip()
        team = 4528615  # the id of the EyeSeeTea team

        url = f'{urlbase}/team/{team}/time_entries'
        req = Request(url, headers={'Authorization': token})

        print(f'Connecting to {urlbase} ...')
        entries = json.loads(urlopen(req).read())['data']
        entries.sort(key=lambda x: x['start'])  # sort by starting date

        for entry in entries:
            print('\n' + info(entry))
    except FileNotFoundError as e:
        print(e)
    except HTTPError as e:
        print(e)
        print('Maybe there is a problem with your token?')


def info(entry):
    "Return a string with information about the entry"
    start_s = int(entry['start']) // 1000  # in seconds since the Epoch
    end_s = int(entry['end']) // 1000
    duration_s = int(entry['duration']) // 1000  # in seconds

    start = datetime.fromtimestamp(start_s).strftime('%a, %d %b %H:%M')
    end = datetime.fromtimestamp(end_s).strftime('%H:%M')
    duration = '%.2f h' % (duration_s / 3600)

    return f"""{start} - {end} ({duration})
{yellow(entry['task']['name'])} {blue(entry['task_url'])}
{green(entry['description'] or '<empty description>')}"""


def ansi(n):
    "Return function that escapes text with ANSI color n"
    return lambda txt: '\x1b[%dm%s\x1b[0m' % (n, txt)

black, red, green, yellow, blue, magenta, cyan, white = map(ansi, range(30, 38))



if __name__ == '__main__':
    main()
