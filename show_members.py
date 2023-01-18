#!/usr/bin/env python3

"""
Show list of user ids and names for the given team.

One can thus find her user id and add it to the configuration file.
"""

import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from configparser import ParsingError

from clickdown import config


def main():
    try:
        cfg = config.init(__doc__)

        url = 'https://api.clickup.com/api/v2/team/' + cfg['team']
        req = Request(url, headers={'Authorization': cfg['token']})

        print('Reading members from %s ...\n' % url)
        members = json.loads(urlopen(req).read())['team']['members']

        print('   user id    user name')
        print('  ----------+------------')
        for x in members:
            print('  %9s   %s' % (x['user']['id'], x['user']['username']))

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



if __name__ == '__main__':
    main()
