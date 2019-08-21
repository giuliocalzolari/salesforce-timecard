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

`password` must be hidden with `base64`

to get `token` please follow this [Guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm)


## Usage
### Help
```bash
  $ timecard --help
  Usage: timecard [OPTIONS] COMMAND [ARGS]...

  Options:
    --version      Show the version and exit.
    -v, --verbose  Will print verbose messages.
    --help         Show this message and exit.

  Commands:
    add
    delete
```

### add

```bash
$ timecard add --help
Usage: timecard add [OPTIONS]

Options:
  -p, --project TEXT              Project Name
  -n, --notes TEXT                Notes to add
  -t, --hours INTEGER             hour/s to add
  --weekday [Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday]
                                  Weekday to add
  -w [|1|2|3|4|5|6|7]             INT Weekday to add
  --help                          Show this message and exit.
```

## Examples

Adding `3` hours of `Personal Developement` on `Wednesday`

```bash
$ timecard add -w 3 -p pdev -t 7
```

Adding `8` hours for proejct `px1234` on `Friday` iwth some `notes`

```bash
$ timecard add -t 7 -p px1234 --weekday Friday --notes "I've done everything!"
```

License
-------

salesforce-timecard is licensed under the [MIT](LICENSE).
