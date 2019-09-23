#!/usr/bin/env python

import sys
import re
import logging
import json
from functools import wraps
import click
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
from collections import OrderedDict
te = TimecardEntry()


contact_id = "0032000001p0EaYAAU"
SQL = '''select Id, Name, pse__Project__c, pse__Project__r.Name, pse__Project__r.pse__Is_Billable__c from pse__Assignment__c 
        where pse__Resource__c = '{}' and 
        pse__Exclude_from_Billing__c = false  and
        pse__Exclude_from_Planners__c = false and
        pse__Closed_for_Time_Entry__c = false
        '''.format(
            contact_id)

results = te.safe_sql(SQL)
assignments = {}
for r in results["records"]:
    print(r["Name"])
    # assignments[r["Id"]] = {"assignment_id": r["Id"], 
    #                         "assignment_name": r["Name"], 
    #                         "project_id": r["pse__Project__c"],
    #                         "project_name": r["pse__Project__r"]["Name"],
    #                         "billable": r["pse__Project__r"]["pse__Is_Billable__c"]}