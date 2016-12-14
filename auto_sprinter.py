__author__ = 'tusharmakkar08'

import datetime
import getpass
import os
import pprint

from jira.client import JIRA


class AutoSprinter:
    def __init__(self):
        self.__server = os.getenv("SERVER")
        self.__username = os.getenv("JIRA_USER")
        self.__password = os.getenv("JIRA_PASS")
        self._options = None
        self._auth = None
        self._jira = None
        self._board_id = os.getenv("JIRA_BOARD_ID")
        self._sprints = []
        self.init_jira()

    def init_jira(self):
        if not self.__server:
            self.__server = raw_input("Enter JIRA server url: \n")
        if not self.__username or not self.__password:
            self.__username = raw_input("Enter JIRA username: ")
            self.__password = getpass.getpass()
        self._options = {"server": self.__server}
        self._auth = (self.__username, self.__password)
        self._jira = JIRA(self._options, basic_auth=self._auth)
        if not self._board_id:
            pprint.pprint(self._jira.boards())
            self._board_id = raw_input("Enter Board Id: ")

    def _create_sprint(self):
        current_date = datetime.datetime.now()
        end_date = (current_date + datetime.timedelta(days=7))
        new_sprint_name = current_date.strftime("%d %B, %Y")
        start_date = current_date.strftime("%d/%b/%y %I:%M %p")
        end_date = end_date.strftime("%d/%b/%y %I:%M %p")
        return self._jira.create_sprint(new_sprint_name,
                                        self._board_id,
                                        startDate=start_date,
                                        endDate=end_date)

    def sprints_update(self):
        self._sprints = self._jira.sprints(self._board_id)
        for sprint in self._sprints:
            if sprint.state == 'ACTIVE':
                future_sprint = self._create_sprint()
                # self._jira.update_sprint(future_sprint.id, state='ACTIVE')


AutoSprinter().sprints_update()
