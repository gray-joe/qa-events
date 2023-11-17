import uuid
from typing import Any

from models.abstract_model import AbstractModel


class PullRequestEventModel(AbstractModel):
    def __init__(self, github_event: dict[str, Any], raw_event_id: int) -> None:
        self.id = uuid.uuid4()
        self.raw_event_id = raw_event_id
        self.build_from_json(github_event)

    def build_from_json(self, github_event: dict[str, Any]) -> None:
        self.project_id = github_event.get("project").get("id")
        self.project_name = github_event.get("project").get("name")
        self.namespaced_project_path = github_event.get("project").get(
            "path_with_namespace"
        )

        self.created_at = github_event.get("object_attributes").get("created_at")
        self.pipeline_id = github_event.get("object_attributes").get("head_pipline_id")
        self.global_mr_id = github_event.get("object_attributes").get("id")
        self.project_mr_id = github_event.get("object_attributes").get("iid")
        self.commit_message = (
            github_event.get("object_attributes").get("last_commit").get("message")
        )
        self.source_branch = github_event.get("object_attributes").get("source_branch")
        self.target_branch = github_event.get("object_attributes").get("target_branch")
        self.title = github_event.get("object_attributes").get("title")
        self.updated_at = github_event.get("object_attributes").get("updated_at")
        self.state = github_event.get("object_attributes").get("state")
        self.action = github_event.get("object_attributes").get("action")
        self.author_id = github_event.get("object_attributes").get("author_id")

    def save(self, database_connection) -> None:
        with database_connection.cursor() as cursor:
            print("Adding new merge request event")
            cursor.execute(
                """
                INSERT INTO merge_request_events(
                    id, project_id, project_name, namespaced_project_path,
                    created_at, pipeline_id, global_mr_id,
                    project_mr_id, commit_message, source_branch, target_branch,
                    title, updated_at, state, action, author_id, raw_event_id
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    str(self.id),
                    self.project_id,
                    self.project_name,
                    self.namespaced_project_path,
                    self.created_at,
                    self.pipeline_id,
                    self.global_mr_id,
                    self.project_mr_id,
                    self.commit_message,
                    self.source_branch,
                    self.target_branch,
                    self.title,
                    self.updated_at,
                    self.state,
                    self.action,
                    self.author_id,
                    self.raw_event_id,
                ),
            )
