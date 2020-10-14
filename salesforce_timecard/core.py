#!/usr/bin/env python

import sys
import logging
import base64
from datetime import datetime, timedelta, date
import os
from simple_salesforce import Salesforce
import json
import keyring

logger = logging.getLogger("salesforce_timecard")


class TimecardEntry(object):

    def __init__(self, cfg="~/.pse.json"):

        self.cfg_file = os.path.expanduser(cfg)
        with open(self.cfg_file) as f:
            self.cfg = json.load(f)

        credential_store = self.cfg.get('credential_store', 'default')
        if credential_store == 'default':
            password = base64.b64decode(self.cfg["password"]).decode()
            security_token = self.cfg["token"]
        elif credential_store == 'keyring':
            password = keyring.get_password("salesforce_cli", f"{self.cfg['username']}_password")
            security_token = keyring.get_password("salesforce_cli", f"{self.cfg['username']}_token")

        self.sf = Salesforce(username=self.cfg["username"],
                             password=password,
                             security_token=security_token,
                             sandbox=self.cfg.get("sandbox", None),
                             client_id="FF"
                             )

        self.contact_id = self.get_contact_id(self.cfg["username"])
        self.assignments = self.get_assignments_active()
        self.global_project = self.get_global_project()
        self.ASSIGNMENTS_MAPPING = []

        today = date.today()
        day = today.strftime("%d-%m-%Y")
        self.get_week(day)

    def get_week(self, day):
        dt = datetime.strptime(day, "%d-%m-%Y")
        self.start = dt - timedelta(days=dt.weekday())
        self.end = self.start + timedelta(days=6)

    def safe_sql(self, sql):
        logger.debug(sql)
        try:
            return self.sf.query_all(sql)
        except:
            logger.error("error on query:{}".format(sql))
            logger.error(sys.exc_info()[1])
            sys.exit(1)

    def list_timecard(self, details, start, end):
        self.assignments = self.get_assignments_all()
        fields = ["Id","Name",  "pse__Project__c", "pse__Assignment__c",
                  "pse__Monday_Hours__c",
                  "pse__Tuesday_Hours__c",
                  "pse__Wednesday_Hours__c",
                  "pse__Thursday_Hours__c",
                  "pse__Friday_Hours__c",
                  "pse__Status__c"]
        if details:
            base = ["OwnerId", "PROJECT_ID__c", "pse__Approved__c", "pse__Start_Date__c", "pse__End_Date__c"]
            fields = base + fields + ["CreatedById", "CreatedDate",  "IsDeleted", "LastModifiedById", "LastModifiedDate",
                               "LastReferencedDate", "LastViewedDate",
                               "pse__Audit_Notes__c", "pse__Billable__c",  "pse__Resource__c",
                               "pse__Location_Mon__c", "pse__Location_Tue__c", "pse__Location_Wed__c",
                               "pse__Location_Thu__c", "pse__Location_Fri__c",
                               "pse__Saturday_Hours__c", "pse__Saturday_Notes__c", "pse__Location_Sat__c",
                               "pse__Sunday_Hours__c", "pse__Sunday_Notes__c", "pse__Location_Sun__c",
                               "pse__Timecard_Notes__c", "pse__Submitted__c",
                               "pse__Monday_Notes__c", "pse__Tuesday_Notes__c",
                               "pse__Wednesday_Notes__c", "pse__Thursday_Notes__c",
                                "pse__Friday_Notes__c"]

        SQL = '''
            select
            {}
            from pse__Timecard_Header__c
            where
            pse__Start_Date__c = {} and pse__End_Date__c = {} and
            pse__Resource__c = '{}' '''.format(
            ", ".join(fields),
            start,
            end,
            self.contact_id,
        )
        results = self.safe_sql(SQL)
        if len(results["records"]) > 0:

            rs = []
            for r in results["records"]:
                r.pop("attributes", None)
                # adding Project name
                if r.get("pse__Assignment__c", "") in self.assignments.keys():
                    r["pse__Project_Name__c"] = self.assignments[r["pse__Assignment__c"]]["assignment_name"]
                if r.get("pse__Project__c", "") in self.global_project.keys():
                    r["pse__Project_Name__c"] = self.global_project[r["pse__Project__c"]]["project_name"]
                rs.append(r)
            return rs
        else:
            logger.warn("No time card")
            return []

    def get_contact_id(self, email):
        name_part = email.split("@")[0]
        r = self.safe_sql(
            "select Id, Name, Email from Contact where pse__Is_Resource__c = true and Email LIKE '{}@%'".format(
                name_part))
        return r["records"][0]["Id"]

    def get_timecard_id(self, timecard_name):
        r = self.safe_sql(
            "select Id from pse__Timecard_Header__c where Name = '{}'".format(
                timecard_name))
        return r["records"][0]["Id"]

    def get_assignments_all(self, contact_id = None):
        if not contact_id:
            contact_id = self.contact_id

        SQL = '''select Id, Name, pse__Project__c, pse__Project__r.Name, pse__Project__r.pse__Is_Billable__c from pse__Assignment__c
        where pse__Resource__c = '{}' and
        Open_up_Assignment_for_Time_entry__c = false and
        pse__Closed_for_Time_Entry__c = false
        '''.format(
            contact_id)

        return self.get_assignments(SQL)

    def get_assignments_active(self, contact_id = None):
        if not contact_id:
            contact_id = self.contact_id

        SQL = '''select Id, Name, pse__Project__c, pse__Project__r.Name, pse__Project__r.pse__Is_Billable__c from pse__Assignment__c
        where pse__Resource__c = '{}' and
        Open_up_Assignment_for_Time_entry__c = false and
        pse__Closed_for_Time_Entry__c = false and
        pse__Exclude_from_Planners__c = false and
        pse__End_Date__c > {}
        '''.format(
            contact_id,
            date.today().strftime("%Y-%m-%d")
            )

        return self.get_assignments(SQL)


    def get_assignments(self, SQL):

        results = self.safe_sql(SQL)
        assignments = {}
        for r in results["records"]:
            assignments[r["Id"]] = {"assignment_id": r["Id"],
                                    "assignment_name": r["Name"],
                                    "project_id": r["pse__Project__c"],
                                    "project_name": r["pse__Project__r"]["Name"],
                                    "billable": r["pse__Project__r"]["pse__Is_Billable__c"]}
        return assignments

    def get_global_project(self):

        SQL = '''select Id, Name, pse__Is_Billable__c
        from pse__Proj__c
        where pse__Allow_Timecards_Without_Assignment__c = true and pse__Is_Active__c = true
        '''
        results = self.safe_sql(SQL)
        rs = {}
        for r in results["records"]:
            rs[r["Id"]] = {
                "project_id": r["Id"],
                "project_name": r["Name"],
                "billable": r["pse__Is_Billable__c"]
            }
        return rs

    def delete_time_entry(self, id):
        try:
            self.sf.pse__Timecard_Header__c.delete(id)
        except:
            logger.error("failed on deletion id:{}".format(id))
            logger.error(sys.exc_info()[1])
            sys.exit(1)

    def add_time_entry(self, assignment_id, day_n, hours, notes):

        self.assignment_id = assignment_id
        new_timecard = {
            "pse__Start_Date__c": self.start.strftime("%Y-%m-%d"),
            "pse__End_Date__c": self.end.strftime("%Y-%m-%d"),
            "pse__Resource__c": self.contact_id,
            "pse__Status__c": "Saved",
        }

        if self.assignment_id in self.assignments.keys():
            new_timecard["pse__Assignment__c"] = self.assignment_id
            new_timecard["pse__Project__c"] = self.assignments[self.assignment_id]["project_id"]
            new_timecard["pse__Billable__c"] = self.assignments[self.assignment_id]["billable"]
            SQL = '''select Id from pse__Timecard_Header__c
                where
                pse__Start_Date__c = {} and pse__End_Date__c = {} and
                pse__Resource__c = '{}' and
                pse__Assignment__c = '{}'  and
                pse__Project__c = '{}' and
                pse__Status__c not in ('Submitted', 'Approved')
                '''.format(
                self.start.strftime("%Y-%m-%d"),
                self.end.strftime("%Y-%m-%d"),
                self.contact_id,
                self.assignment_id,
                self.assignments[self.assignment_id]["project_id"],
            )
        else:
            # most probably is a project without assigment
            new_timecard["pse__Project__c"] = self.assignment_id
            new_timecard["pse__Billable__c"] = self.global_project[self.assignment_id]["billable"]
            SQL = '''select Id from pse__Timecard_Header__c
                where
                pse__Start_Date__c = {} and pse__End_Date__c = {} and
                pse__Resource__c = '{}' and
                pse__Project__c = '{}' and
                pse__Status__c not in ('Submitted', 'Approved')
                '''.format(
                self.start.strftime("%Y-%m-%d"),
                self.end.strftime("%Y-%m-%d"),
                self.contact_id,
                self.assignment_id,
            )

        new_timecard["pse__" + day_n + "_Hours__c"] = hours
        new_timecard["pse__" + day_n + "_Notes__c"] = notes

        results = self.safe_sql(SQL)
        logger.debug(json.dumps(new_timecard, indent=4))
        if len(results["records"]) > 0:
            logger.debug("required update")
            try:
                self.sf.pse__Timecard_Header__c.update(
                    results["records"][0]["Id"], new_timecard)
            except:
                logger.error("failed on update")
                logger.error(sys.exc_info()[1])
                sys.exit(1)

        else:
            try:
                self.sf.pse__Timecard_Header__c.create(new_timecard)
            except:
                logger.error("failed on creation")
                logger.error(sys.exc_info()[1])
                sys.exit(1)

    def submit_time_entry(self, id):
        data = {
            "pse__Submitted__c": True,
            "pse__Status__c": "Submitted",

        }
        try:
            self.sf.pse__Timecard_Header__c.update(id, data)
        except:
            logger.error("failed on update")
            logger.error(sys.exc_info()[1])
            sys.exit(1)
