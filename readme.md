# Clickdown

Utilities to work with [clickup](https://clickup.com/).

They work by making queries to the clickup api. The requests are
cached for an hour, but you can delete the cache files at any point.

To run them, you need a configuration file named `clickdown.cfg` that
contains at least your clickup token (see section `Getting a token`
below) and the id of your team.


## Clicktime

Shows information for the time tracked in tasks during the last month.

Run it with:

```sh
./clicktime.py
```

It prints in the console something like:

```
Connecting to https://api.clickup.com/api/v2/team/1234567/time_entries ...
Caching result for the next hour in /home/you/.cache/clickdown/time.json ...

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
Connecting to https://api.clickup.com/api/v2/team/1234567/task?assignees[]=12345678 ...
Caching result for the next hour in /home/you/.cache/clickdown/tasks.json ...

# 1 (in progress) Fun list https://app.clickup.com/t/4hfw59n
Create new system to conquer the world

# 2 (to do) Boring list https://app.clickup.com/t/1u654a9
Find subtle bug in unreadable, clumsy, slow software

[...]

>
```

and you can input the number of a task to see more details about it.


## Configuration file

The configuration file is named `clickdown.cfg` and looks like this:

```cfg
token = YOUR_TOKEN

# The id of your team.
team = 1234567

# The id of your user.
user = 12345678
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

One possible way is to find it in the output of:

```sh
http https://api.clickup.com/api/v2/team/YOUR_TEAM_ID 'Authorization: YOUR_TOKEN' | \
    jq -c '.team.members[].user | {id, username}'
```

(This example uses [httpie](https://httpie.io/) and
[jq](https://stedolan.github.io/jq/).)


## Clickup api

Reference about the clickup api: https://clickup.com/api

In particular, these are the endpoints for each program:

* clicktime - https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/
* clicktasks - https://clickup.com/api/clickupreference/operation/GetFilteredTeamTasks/
