# `salesforce-timecard`

[![PyPI version](https://badge.fury.io/py/salesforce-timecard.svg)](https://badge.fury.io/py/salesforce-timecard)
[![Actions Status: test](https://github.com/giuliocalzolari/salesforce-timecard/actions/workflows/test.yml/badge.svg)](https://github.com/giuliocalzolari/salesforce-timecard/actions?query=workflow%3A"Python%20testing")
[![Actions Status: publish](https://github.com/giuliocalzolari/salesforce-timecard/actions/workflows/publish.yml/badge.svg)](https://github.com/giuliocalzolari/salesforce-timecard/actions?query=workflow%3A"Publish%20PyPi")


This Python package provides a CLI tool which can submit timecard entries to
SalesForce programmatically.

## Installation

To install the tool from PyPI, just use `pip`:

```bash
pip install salesforce-timecard
```

Or better use [pipx](https://github.com/pipxproject/pipx)

```
pipx install salesforce-timecard
```

## Configuration

The script requires a local configuration file with your SalesForce credentials
included in it, located at `~/.pse.json`. It should look like:

```json
{
  "username": "your-salesforce-email@example.com",
  "password": "yoursupersecretpasswd",
  "token": "afghfyfgbgnegrfbgdhtd"
}
```


To obtain the security token for your Salesforce account, follow
[this guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm).

### Password Alternatives

It is also possible to store password & security token in your OS' keyring. This supports any backends listed by the [Python keyring library](https://pypi.org/project/keyring).

To do so, your config file (`~/.pse.json`) should contain just `username` and `credential_store` values:
```json
{
  "username": "your-salesforce-email@example.com",
  "credential_store": "keyring"
}
```

Default values for the keyring assume everything is stored under the `salesforce_cli` application in your keyring. Your password would be stored as a `salesforce_cli` item with username `your-salesforce-email@example.com_password`, while the security token would be stored as `salesforce_cli`, `your-salesforce-email@example.com_token`.

Under MacOS this can be added with the "Keychain Access" application, under the default "login" keychain. `salesforce_cli` is the Keychain Item Name for both instances, and the `your-salesforce-email@example.com_password` or `your-salesforce-email@example.com_token` string is the Account Name.

## Examples

Adding 3 hours of personal development on Wednesday:

```
$ timecard add -w 3 -p pdev -t 7
```

Adding entries from a file:
1. Create a `timecard.yaml` file with a sample content `timecard sample > this_week.yaml`
2. Edit `timecard.yaml`
3. Add your timecard `timecard add -f timecard.yaml`

Adding 8 hours for project PX1234 on Friday with some notes:

```
$ timecard add -t 7 -p px1234 --weekday Friday --notes "I've done everything!"
```

Deleting timecard directly:

```
$ timecard delete TCH-08-21-2019-078970
Do you want to delete the timecard TCH-08-21-2019-078970 ? [y/N]: y
[2019-08-21 14:08:04,917][INFO] timecard TCH-08-21-2019-078970 deleted
```

Or interactively:

```
$ timecard delete
Please choose which timecard:
[0] TCH-08-20-2019-078900 projectA
[1] TCH-08-21-2019-078950 projectB
[2] TCH-08-21-2019-078956 projectC
Selection: 2
Do you want to delete the timecard TCH-08-21-2019-078956 ? [y/N]: y
[2019-08-21 14:08:04,917][INFO] timecard TCH-08-21-2019-078956 deleted
```

Listing timecards for a specific week with debug information:

```
$ timecard -s 2019-08-19 -e 2019-08-25 list
$ timecard --week -1 list
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

Listing timecards for this week:

```
$ timecard ls
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

Submitting timecards for this week (on Friday for example):

```
$ timecard submit
TCH-08-26-2019-079767 - Project 1
TCH-08-26-2019-079768 - Project 2
TCH-08-26-2019-079769 - Project 3
Do you want to submit all timecard ? [Y/n]:
timecard TCH-08-26-2019-079767 submitted
timecard TCH-08-26-2019-079768 submitted
timecard TCH-08-26-2019-079769 submitted
```

## TODO

-   Clean up remaining documentation
-   Run linter over the code
-   Setup tool for initial config file generation / keychain seeding

## License

`salesforce-timecard` is licensed under the [WTFPL](LICENSE).
