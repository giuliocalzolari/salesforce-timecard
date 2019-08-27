# PSE Timecard Entry


[![PyPI version](https://badge.fury.io/py/salesforce-timecard.svg)](https://badge.fury.io/py/salesforce-timecard)
[![Build Status](https://api.travis-ci.org/giuliocalzolari/salesforce-timecard.svg?branch=master)](https://travis-ci.org/giuliocalzolari/salesforce-timecard/)

## Install
just use pip

```bash
$ pip install salesforce-timecard
```

## Config
this script is designed to create a pse_timecard

create your local Config `~/.pse_timecard.json`

```bash
  {
    "username": "your-salesforce-email@login.com",
    "password": "fdgdhrx6MA==",
    "token": "afghfyfgbgnegrfbgdhtd"
  }
```

`password` must be `base64` encoded

```bash
$ echo -n "my-password" | base64
```

to get `token` please follow this [Guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm)

## Examples

Adding `3` hours of `Personal Developement` on `Wednesday`

```bash
$ timecard add -w 3 -p pdev -t 7
```

Adding `8` hours for proejct `px1234` on `Friday` iwth some `notes`

```bash
$ timecard add -t 7 -p px1234 --weekday Friday --notes "I've done everything!"
```

Deleting timecard with `argument` or with interactive input

```bash
$ timecard delete TCH-08-21-2019-078970
Do you want to delete the timecard TCH-08-21-2019-078970 ? [y/N]: y
[2019-08-21 14:08:04,917][INFO] timecard TCH-08-21-2019-078970 deleted

$ timecard delete 
Please choose which timecard:
[0] TCH-08-20-2019-078900 projectA
[1] TCH-08-21-2019-078950 projectB
[2] TCH-08-21-2019-078956 projectC
Selection: 2
Do you want to delete the timecard TCH-08-21-2019-078956 ? [y/N]: y
[2019-08-21 14:08:04,917][INFO] timecard TCH-08-21-2019-078956 deleted

```


List timecard of specific week with `debug`

```bash
$ timecard -v -s 2019-08-19 -e 2019-08-25 list
$ timecard -v --week -1 list
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
|         Name          |   Monday |   Tuesday |   Wednesday |   Thursday |   Friday |  Status  |             Project_Name              |   SUM |
+=======================+==========+===========+=============+============+==========+==========+=======================================+=======+
| TCH-08-20-2019-078900 |        7 |         0 |           3 |          0 |        0 | Approved | Internal Process Systems Improvements |    10 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
| TCH-08-21-2019-078950 |        0 |         5 |           3 |          3 |        3 | Approved |            Team Management            |    14 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
| TCH-08-21-2019-078956 |        1 |         3 |           2 |          3 |        3 | Approved |         Personal Development          |    12 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
| TCH-08-22-2019-079068 |        0 |         0 |           0 |          2 |        2 | Approved |               Presales                |     4 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
|         Total         |        8 |         8 |           8 |          8 |        8 |          |                                       |    40 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+---------------------------------------+-------+
```

List timecard of this week

```bash
$ timecard list
+-----------------------+----------+-----------+-------------+------------+----------+----------+-----------------------------+-------+
|         Name          |   Monday |   Tuesday |   Wednesday |   Thursday |   Friday |  Status  |        Project_Name         |   SUM |
+=======================+==========+===========+=============+============+==========+==========+=============================+=======+
| TCH-08-26-2019-079767 |        2 |         2 |           0 |          0 |        0 |  Saved   | Internal - Events and Blogs |     4 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+-----------------------------+-------+
| TCH-08-26-2019-079768 |        4 |         0 |           0 |          0 |        0 |          |    Personal Development     |     4 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+-----------------------------+-------+
| TCH-08-26-2019-079769 |        2 |         0 |           0 |          3 |        0 |  Saved   |       Team Management       |     5 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+-----------------------------+-------+
|         Total         |        8 |         2 |           0 |          3 |        0 |          |                             |    13 |
+-----------------------+----------+-----------+-------------+------------+----------+----------+-----------------------------+-------+
```

# License


salesforce-timecard is licensed under the [Apache 2.0](LICENSE).
