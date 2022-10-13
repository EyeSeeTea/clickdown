# Clickup time track

Shows information for the time tracked in tasks during the last month.

To run it, you need to have a file called `token.txt` that contains
your clickup token (see section `Getting a token` below).

Run it with:

```sh
./clickup.py
```

It will print in the console something like:

```
Connecting to https://api.clickup.com/api/v2 ...

Mon, 19 Sep 09:00 - 11:00 (2.00 h)
Server optimization https://app.clickup.com/t/253hjxz
Rewired the servers for max fun

Mon, 19 Sep 12:00 - 14:00 (2.00 h)
Boring task #666 https://app.clickup.com/t/133hgxs
Watched paint dry

[...]
```


## Getting a token

The program connects to clickup on your behalf. To do so, it needs to
use a personal token that identifies you.

To get a token, go to clickup -> user (bottom left) -> Apps. See the
detailed documentation at:
https://clickup.com/api/developer-portal/authentication/#personal-token

Once you have a token, you just need to write it into a file called
`token.txt` for the program to read it.


## Clickup api

Reference about the clickup api:
https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/
