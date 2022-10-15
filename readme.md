# Clickdown

Utilities to work with [clickup](https://clickup.com/).

They work by making queries to the clickup api. The requests are
cached for an hour, but you can delete the cache files at any point.


## Clicktime

Shows information for the time tracked in tasks during the last month.

To run it, you need a file named `token.txt` that contains your
clickup token (see section `Getting a token` below).

Run it with:

```sh
./clicktime.py
```

It prints in the console something like:

```
Reading token from local file token.txt ...
Connecting to https://api.clickup.com/api/v2/team/1234567/time_entries ...
Caching result for the next hour to /home/you/.cache/clickdown/time.json ...

== Mon 19 Sep (total: 4.00 h) ==

09:00 - 11:00 (2.00 h)
Server optimization https://app.clickup.com/t/253hjxz
Rewired the servers for max fun

12:00 - 14:00 (2.00 h)
Boring task #666 https://app.clickup.com/t/133hgxs
Watched paint dry

== Tue 20 Sep (total: 6.25 h) ==

[...]
```


## Clicktasks

Shows the tasks assigned to you.

Run it with:

```sh
./clicktasks.py
```

It prints in the console something like:

```
Reading token from /home/you/.config/clickdown/token.txt ...
Connecting to https://api.clickup.com/api/v2/team/1234567/task?assignees[]=12345678 ...
Caching result for the next hour to /home/you/.cache/clickdown/tasks.json ...

# 1 (in progress) Fun list https://app.clickup.com/t/4hfw59n
Create new system to conquer the world

# 2 (to do) Boring list https://app.clickup.com/t/1u654a9
Find subtle bug in unreadable, clumsy, slow software

[...]

>
```

and you can input the number of a task to see more details about it.


## Getting a token

The programs connect to clickup on your behalf. To do so, they need to
use a personal token that identifies you.

To get a token, go to clickup -> user (bottom left) -> Apps. See the
detailed documentation at
https://clickup.com/api/developer-portal/authentication/#personal-token

You can write the token in a file named `token.txt` for the programs
to read it. The file can be in the directory where you run the
programs, or in its [standard configuration
directory](https://en.wikipedia.org/wiki/Freedesktop.org#Base_Directory_Specification)
(normally `$HOME/config/clickdown`).


## Clickup api

Reference about the clickup api: https://clickup.com/api

In particular, these are the endpoints for each program:

* clicktime - https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/
* clicktasks - https://clickup.com/api/clickupreference/operation/GetFilteredTeamTasks/
