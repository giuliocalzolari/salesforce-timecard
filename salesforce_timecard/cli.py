#!/usr/bin/env python

import sys
import logging
import json
from functools import wraps
import click
from datetime import datetime as date
from salesforce_timecard.core import TimecardEntry
from salesforce_timecard import __version__, __description__

logger = logging.getLogger("salesforce_timecard")
handler = logging.StreamHandler(sys.stdout)
FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

te = TimecardEntry()


def catch_exceptions(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        Invokes ``func``, catches expected errors, prints the error message and
        exits sceptre with a non-zero exit code.
        """
        try:
            return func(*args, **kwargs)
        except:
            logger.error(sys.exc_info()[1])
            sys.exit(1)

    return decorated


@click.group()
@click.version_option(prog_name=__description__, version=__version__)
@click.option('-v', '--verbose', is_flag=True, help="verbose")
@click.pass_context
def cli(ctx, verbose):  # pragma: no cover
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("enabling DEBUG mode")
    ctx.obj = {
        "options": {},
    }
    pass


@cli.command(name="delete")
@click.argument('secret')
@click.pass_context
@catch_exceptions
def delete(ctx, secret):
    logger.info("delete action TODO")
    sys.exit(1)
    # if click.confirm(
    #         "Do you want to delete the secret {} ?".format(secret),
    #         abort=True):
    #     if EC2stash(ctx.obj).delete_parameter(secret):
    #         logger.info("secret {} deleted".format(secret))
    #     else:
    #         logger.error("secret {} NOT deleted".format(secret))
    # else:
    #     logger.info("Abort: secret {} not delete".format(secret))

@cli.command(name="list")
@click.option('--details/--no-details', default=False)
@click.option(
    "-s", "--startday", default=te.start.strftime('%Y-%m-%d'), help="Start day")
@click.option(
    "-e", "--endday", default=te.end.strftime('%Y-%m-%d'), help="End day")    
@click.pass_context
@catch_exceptions
def list(ctx, details, startday, endday):
    rs = te.list_timecard(details, startday, endday)
    click.echo(json.dumps(rs, indent=4))


@cli.command(name="add")
@click.option(
    "-p", "--project", default="", help="Project Name")
@click.option(
    "-n", "--notes", default="Business as usual", help="Notes to add")
@click.option(
    "-t", "--hours", default=0, help="hour/s to add")
@click.option(
    "--weekday",
    type=click.Choice(['Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday', 'Sunday']),
    default=date.today().strftime("%A"),
    help="Weekday to add")
@click.option(
    "-w",
    type=click.Choice(["", "1", "2", "3", "4", "5", "6", "7"]),
    default="",
    help="INT Weekday to add")
@click.pass_context
@catch_exceptions
def add(ctx, project, notes, hours, weekday, w):
    assignment_id = None

    for _, assign in te.assignments.items():
        if project.lower() in assign["project_name"].lower() and len(project) > 4:
            logger.info("found " + assign["project_name"])
            assignment_id = assign["assignment_id"]

    if project.lower() in [ "pdev", "personal development", "development"]:
        assignment_id = "a7O0J000000PN8jUAG" #manual hack

    if not assignment_id:
        nice_assign = []
        i = 0
        print("Please choose which project:")
        for _, assign in te.assignments.items():
            print("[{}] {}".format(i, assign["project_name"]))
            nice_assign.append(assign["assignment_id"])
            i += 1
        select_assign = input("Selection: ")
        assignment_id = nice_assign[int(select_assign)]

    if w != "":
        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_n_in = days[int(w) - 1]
    else:
        day_n_in = weekday

    if hours == 0:
        _hours = input("hours (default 8): ")
        print(_hours)
        if not _hours:
            hours_in = 8
        else:
            hours_in = _hours
    else:
        hours_in = hours

    te.add_time_entry(assignment_id, day_n_in, hours_in, notes)


if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    cli()
