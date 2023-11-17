from typing import Any, Union

from models.abstract_model import AbstractModel
from models.jira_ticket_events_model import JiraTicketEventsModel
from models.merge_request_events_model import MergeRequestEventModel
from models.pipeline_jobs_model import PipelineJobsModel


class GitlabModelFactory:
    @classmethod
    def make(cls, gitlab_event: dict[str, Any], raw_event_id: int) -> Union[AbstractModel, bool]:
        if gitlab_event.get("object_kind") == "build":
            print("Webhook event identified: pipeline job")
            return PipelineJobsModel(gitlab_event, raw_event_id)
        if gitlab_event.get("object_kind") == "merge_request":
            print("Webhook event identified: merge request event")
            return MergeRequestEventModel(gitlab_event, raw_event_id)
        print(f"Current event: {gitlab_event.get('object_kind')} does not have an associated model")
        return False


class JiraModelFactory:
    @classmethod
    def make(cls, jira_event: dict[str, Any], raw_event_id: int) -> Union[AbstractModel, bool]:
        if jira_event.get("issue_event_type_name") in ["issue_created", "issue_updated", "issue_deleted", "issue_generic", "issue_moved"]:
            print("Webhook event identified: Jira ticket event")
            return JiraTicketEventsModel(jira_event, raw_event_id)
        print("Webhook does not match any Jira models")
        return False
