#!/usr/bin/env python

import sys
import re
import logging
import json
import yaml
from functools import wraps
import click
from click_aliases import ClickAliasedGroup
from tabulate import tabulate
from datetime import datetime, timedelta, date
from salesforce_timecard.core import TimecardEntry
from salesforce_timecard.utils import HoursCounter
from salesforce_timecard import __version__, __description__

logger = logging.getLogger("salesforce_timecard")
handler = logging.StreamHandler(sys.stdout)
FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

te = TimecardEntry()


def process_row(ctx, project, notes, hours, weekday, w, file):
    assignment_id = None
    active_assignment = te.get_assignments_active()
    for _, assign in active_assignment.items():
        if project.lower() in assign["assignment_name"].lower() and len(project) > 2:
            logger.info("found :{}".format(assign["assignment_name"]))
            assignment_id = assign["assignment_id"]
            break

    if project.lower() in ["pdev", "personal development", "development"]:
        project = "Personal Development"  # manual hack

    if project.lower() in ["pto", "holiday", "off"]:
        project = "Time Off"  # manual hack

    if not assignment_id:
        # fetch global project
        global_project = te.global_project
        for _, prj in global_project.items():
            if project.lower() in prj["project_name"].lower() and len(project) > 4:
                logger.info("found " + prj["project_name"])
                assignment_id = prj["project_id"]
                break

    if not assignment_id:
        nice_assign = []
        i = 0
        click.echo("Please choose which project:")
        for _, assign in active_assignment.items():
            click.echo("[{}] {}".format(i, assign["assignment_name"]))
            nice_assign.append(assign["assignment_id"])
            i += 1

        click.echo()
        click.echo("Global Project")
        for _, prj in global_project.items():
            click.echo("[{}] {}".format(i, prj["project_name"]))
            nice_assign.append(prj["project_id"])
            i += 1

        select_assign = input("Selection: ")
        assignment_id = nice_assign[int(select_assign)]

    if w != "":
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        day_n_in = days[int(w) - 1]
    else:
        day_n_in = weekday

    if hours == 0:
        _hours = input("hours (default 8): ")
        hours_in = 8 if not _hours else _hours
    else:
        hours_in = hours

    te.add_time_entry(assignment_id, day_n_in, hours_in, notes)
    logger.info("Time card added")


def catch_exceptions(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        Invokes ``func``, catches expected errors, prints the error message and
        exits sceptre with a non-zero exit code.
        """
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            click.echo(" bye bye")
        except:
            if len(str(sys.exc_info()[1])) > 0:
                logger.error(sys.exc_info()[1])
                sys.exit(1)

    return decorated


@click.group(cls=ClickAliasedGroup)
@click.version_option(prog_name=__description__, version=__version__)
@click.option("-v", "--verbose", is_flag=True, help="verbose")
@click.option(
    "-s", "--startday", default=te.start.strftime("%Y-%m-%d"), help="Start day")
@click.option(
    "-e", "--endday", default=te.end.strftime("%Y-%m-%d"), help="End day")
@click.option(
    "--week", default="", help="relative week interval e.g.: -1")
@click.pass_context
def cli(ctx, verbose, startday, endday, week):  # pragma: no cover

    regex = r"^([2][0]\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$"
    if not re.match(regex, startday):
        click.echo("INVALID start date - please use YYYY-MM-DD format")
        sys.exit(1)

    if not re.match(regex, endday):
        click.echo("INVALID end date - please use YYYY-MM-DD format")
        sys.exit(1)

    if week != "":
        day = date.today().strftime("%Y-%m-%d")
        dt = datetime.strptime(day, "%Y-%m-%d")
        _startday = dt - timedelta(days=dt.weekday()) + timedelta(weeks=int(week))
        _endday = _startday + timedelta(days=6)
        startday = _startday.strftime("%Y-%m-%d")
        endday = _endday.strftime("%Y-%m-%d")

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("enabling DEBUG mode")
    ctx.obj = {
        "options": {},
        "startday": startday,
        "endday": endday
    }


@cli.command(name="delete", aliases=["d", "del", "rm", "remove"])
@click.argument("timecard", required=False)
@click.pass_context
@catch_exceptions
def delete_cmd(ctx, timecard):
    """Delete time entry from a timecard."""

    if not timecard:
        rs = te.list_timecard(False, ctx.obj["startday"], ctx.obj["endday"])
        i = 0
        nice_tn = []
        click.echo("Please choose which timecard:")
        for timecard_rs in rs:
            click.echo("[{}] {} - {}".format(i,
                                             timecard_rs["Name"],
                                             timecard_rs.get(
                                                 "pse__Project_Name__c", "")
                                             )
                       )
            nice_tn.append(
                {"Id": timecard_rs["Id"], "Name": timecard_rs["Name"]})
            i += 1
        select_tmc = input("Selection: ")
        timecard_id = nice_tn[int(select_tmc)]["Id"]
        timecard_name = nice_tn[int(select_tmc)]["Name"]
    else:
        timecard_id = te.get_timecard_id(timecard)
        timecard_name = timecard

    if click.confirm(
            "Do you want to delete the timecard: {} {}?".format(
                timecard_name,
                timecard_rs.get("pse__Project_Name__c", "")
            ),
            abort=True):
        te.delete_time_entry(timecard_id)
        logger.info("timecard {} deleted".format(timecard_name))


@cli.command(name="submit", aliases=["s", "send"])
@click.option("-f", "--force", default=False, is_flag=True, help="confirm all question")
@click.pass_context
@catch_exceptions
def submit(ctx, force):
    """Submit timecard."""
    rs = te.list_timecard(False, ctx.obj["startday"], ctx.obj["endday"])
    tc_ids = []
    for timecard_rs in rs:
        click.echo("{} - {}".format(timecard_rs["Name"],
                                    timecard_rs.get(
                                            "pse__Project_Name__c", "")
                                        )
                )
        tc_ids.append(timecard_rs)

    if not force:
            click.confirm("Do you want to submit all timecard ?", default=True, abort=True)
            click.echo()

    for tc in tc_ids:
        te.submit_time_entry(tc["Id"])
        logger.info("timecard {} submitted".format(tc["Name"]))


@cli.command(name="list", aliases=["ls", "lst", "l"])
@click.option("--details/--no-details", default=False)
@click.option(
    "--style",
    type=click.Choice(["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "jira", "presto", "json"]),
    default="grid",
    help="table style")
@click.pass_context
@catch_exceptions
def list(ctx, details, style):
    rs = te.list_timecard(details, ctx.obj["startday"], ctx.obj["endday"])
    if style == "json":
        click.echo(json.dumps(rs, indent=4))
    else:
        hc = HoursCounter(rs)
        click.echo(tabulate(hc.report, headers="keys", tablefmt=style, stralign="center", ))



@cli.command(name="add", aliases=["a", "ad"])
@click.option(
    "-p", "--project", default="", help="Project Name")
@click.option(
    "-n", "--notes", default="Business as usual", help="Notes to add")
@click.option(
    "-t", "--hours", default=0, help="hour/s to add")
@click.option(
    "--weekday",
    type=click.Choice(["Monday", "Tuesday", "Wednesday",
                       "Thursday", "Friday", "Saturday", "Sunday"]),
    default=date.today().strftime("%A"),
    help="Weekday to add")
@click.option(
    "-w",
    type=click.Choice(["", "1", "2", "3", "4", "5", "6", "7"]),
    default="",
    help="INT Weekday to add")
@click.option(
    "-f", "--file", default="", help="YAML file containing timesheet data")
@click.pass_context
@catch_exceptions
def add(ctx, project, notes, hours, weekday, w, file):
    """Add time entry to the timecard."""
    # hack to let the option call the verb recursively
    if file != "":
        click.echo(f"Parsing timesheet file {file}...")
        with open(file, "r") as stream:
            bulk_data = yaml.safe_load(stream)

        click.echo(bulk_data)
        for day, work in bulk_data.items():
            click.echo(f"Adding entries for {day}...")
            for task, meta in work.items():
                notes = meta['notes'] if 'notes' in meta else ''
                process_row(ctx, task, notes, meta['hours'], day, '', '')
    else:
        process_row(ctx, project, notes, hours, weekday, w, file)


@cli.command(name="sample-timecard", aliases=["sample"])
def sample_timecard():
    """Print example timecard.yaml."""
    click.echo(
        yaml.safe_dump(
            {
                "Monday": {
                    "Project Name 1": {
                        "notes": "Some note for the project/day",
                        "hours": 8,
                    }
                },
                "Tuesday": {"Project Name 1": {"hours": 8}},
                "Wednesday": {"Project Name 1": {"hours": 8}},
                "Thursday": {"Project Name 1": {"hours": 8}},
                "Friday": {
                    "Project Name 2": {
                        "hours": 4,
                        "notes": "Working on Giulio's SalesForce CLI tool",
                    },
                    "Project Name 3": {"hours": 4},
                },
            },
            sort_keys=False,
        )
    )


@cli.command(name="sample-cfg", aliases=["cfg"])
def sample_timecard():
    """Print example .pse.json"""
    click.echo(
        json.dumps({
            "username": "YourName@example.com",
            "credential_store": "keyring"
        }, indent = 4)
    )