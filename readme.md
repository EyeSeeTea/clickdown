# Clickdown

Utilities to work with [clickup](https://clickup.com/).

* `time.py` shows your tracked time
* `tasks.py` shows your tasks

They work by making queries to the clickup api. The responses are
cached for some time (an hour by default), but you can force a reload
or delete the cache files at any point.

To run you need a configuration file named `clickdown.cfg` that
contains at least your clickup token and the id of your team (see
section `Configuration file` below).


## time

Shows information for your time tracked in tasks during the last month.

Run it with:

```sh
./time.py
```

It prints in the console something like:

```
Connecting to https://api.clickup.com/api/v2/team/1234567/time_entries ...
Caching result in /home/you/.cache/clickdown/time.json ...

Showing entries for the last 14 days:

== Mon 19 Sep (total: 4.0 h) ==

09:00 - 11:00 (2.00 h)
Server optimization https://app.clickup.com/t/253hjxz
Rewired the servers for max fun

12:00 - 14:00 (2.00 h)
Boring task #666 https://app.clickup.com/t/133hgxs
Watched paint dry

== Tue 20 Sep (total: 6.2 h) ==

[...]
```


## tasks

Shows the tasks assigned to you.

Run it with:

```sh
./tasks.py
```

It prints in the console something like:

```
Connecting to https://api.clickup.com/api/v2/team/1234567/task?assignees[]=12345678 ...
Caching result in /home/you/.cache/clickdown/tasks.json ...

# 1 Create new system to conquer the world
Fun list - in progress - https://app.clickup.com/t/4hfw59n

# 2 Find subtle bug in unreadable, clumsy, slow software
Boring list - to do - https://app.clickup.com/t/1u654a9

[...]

View task details (you can select by number or by name, use arrows, tab, Ctrl+r, etc.):
>
```

and you can input the number or the name of a task to see more details
about it.


## Configuration file

The configuration file is named `clickdown.cfg` and looks like this:

```conf
# Your clickup token (necessary). In: clickup -> user (bottom left) -> Apps.
token = YOUR_TOKEN

# The id of your team (necessary). In: https://app.clickup.com/{team}
team = 1234567

# The id of your user (necessary only if you use tasks).
user = 12345678

# Comma-separated list of status of tasks to ignore (in tasks, optional).
ignored = to test,blocked,done (to be reviewed)

# Maximum number of seconds to keep the cached files (optional, 1h by default).
cache_age_max = 3600

# Maximum number of days to show (in time, optional, 14 by default, 30 maximum).
days_max = 14

# Color theme (optional, can be "light", "dark" (default), or "none").
theme = dark
```

### Getting a token

The programs connect to clickup on your behalf. To do so, they need to
use a personal token that identifies you.

To [get a
token](https://clickup.com/api/developer-portal/authentication/#personal-token),
basically go to clickup -> user (bottom left) -> Apps.


### Finding your team id

Your team id is the number that appears just after `app.clickup.com`
in your browser bar when you are logged in.


### Finding your user id

If you have your `team` id and `token` already in `clickdown.cfg`, you
can find your user id by looking at the output of:

```sh
./show_members.py
```


## Clickup api

Reference about the clickup api: https://clickup.com/api

In particular, these are the endpoints for each program:

* time - https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/
* tasks - https://clickup.com/api/clickupreference/operation/GetFilteredTeamTasks/
