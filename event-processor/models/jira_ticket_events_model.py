import uuid
from datetime import datetime
from typing import Any

from models.abstract_model import AbstractModel


class JiraTicketEventsModel(AbstractModel):
    def __init__(self, jira_event: dict[str, Any], raw_event_id: int) -> None:
        self.id = uuid.uuid4()
        self.raw_event_id = raw_event_id
        self.build_from_json(jira_event)

    def build_from_json(self, jira_event: dict[str, Any]) -> None:
        self.id = uuid.uuid4()
        self.event_timestamp = datetime.fromtimestamp(jira_event.get('timestamp')/1000)
        self.issue_id = jira_event.get('issue').get('id')
        self.issue_key = jira_event.get('issue').get('key')
        self.issue_type_name = jira_event.get('issue').get('fields').get('issuetype').get('name')
        self.project_key = jira_event.get('issue').get('fields').get('project').get('key')
        self.updated_at = jira_event.get('issue').get('fields').get('updated')
        self.status_name = jira_event.get('issue').get('fields').get('status').get('name')
        self.created_at = jira_event.get('issue').get('fields').get('created')
        self.team = jira_event.get('issue').get('fields').get('customfield_10001').get('name')

    def save(self, database_connection) -> None:
        with database_connection.cursor() as cursor:
            print("Adding new jira ticket event")
            cursor.execute(
                """
                INSERT INTO jira_ticket_events(
                    id, event_timestamp, issue_id, issue_key, issue_type_name,
                    project_key, updated_at, status_name, created_at, team, raw_event_id
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    str(self.id),
                    self.event_timestamp, self.issue_id, self.issue_key, self.issue_type_name,
                    self.project_key, self.updated_at, self.status_name, self.created_at, self.team,
                    self.raw_event_id
                ),
            )
