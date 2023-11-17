import re
import uuid
from typing import Any

from models.abstract_model import AbstractModel


class PipelineJobsModel(AbstractModel):
    def __init__(self, gitlab_event: dict[str, Any], raw_event_id: int) -> None:
        self.id = uuid.uuid4()
        self.raw_event_id = raw_event_id
        self.build_from_json(gitlab_event)

    def build_from_json(self, gitlab_event: dict[str, Any]) -> None:
        self.merge_request_id = None
        if gitlab_event.get("ref") and re.match(
            "\w+/\w+-\w+/(\d+)/\w+", gitlab_event.get("ref")
        ):
            self.merge_request_id = re.search(
                "\w+/\w+-\w+/(\d+)/\w+", gitlab_event.get("ref")
            ).group(1)

        self.job_id = gitlab_event.get("build_id")
        self.name = gitlab_event.get("build_name")
        self.stage = gitlab_event.get("build_stage")
        self.status = gitlab_event.get("build_status")

        self.created_at = gitlab_event.get("build_created_at")
        self.started_at = gitlab_event.get("build_started_at")
        self.finished_at = gitlab_event.get("build_finished_at")
        self.duration = (
            round(gitlab_event.get("build_duration"))
            if gitlab_event.get("build_duration", "") not in ["", None]
            else None
        )
        self.queued_duration = (
            round(gitlab_event.get("build_queued_duration"))
            if gitlab_event.get("build_queued_duration", "") not in ["", None]
            else None
        )

        self.failure_reason = gitlab_event.get("build_failure_reason")

        self.pipeline_id = gitlab_event.get("pipeline_id")
        self.runner_description = ""
        self.runner_tags = ""
        if gitlab_event.get("runner") is not None:
            self.runner_description = gitlab_event.get("runner", {}).get(
                "description", ""
            )
            self.runner_tags = ",".join(gitlab_event.get("runner", {}).get("tags", []))

        self.project_id = gitlab_event.get("project_id")
        self.project_name = gitlab_event.get("project_name")
        self.merge_commit_message = gitlab_event.get('commit', {}).get('message', '')

    def save(self, database_connection) -> None:
        with database_connection.cursor() as cursor:
            print("Adding new pipeline job")
            cursor.execute(
                """
                INSERT INTO pipeline_jobs(
                    id, merge_request_id, job_id, name, stage, status, 
                    created_at, started_at, finished_at, duration, queued_duration, 
                    failure_reason, pipeline_id, runner_description, runner_tags, 
                    project_id, project_name, merge_commit_message, raw_event_id
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    str(self.id),
                    self.merge_request_id,
                    self.job_id,
                    self.name,
                    self.stage,
                    self.status,
                    self.created_at,
                    self.started_at,
                    self.finished_at,
                    self.duration,
                    self.queued_duration,
                    self.failure_reason,
                    self.pipeline_id,
                    self.runner_description,
                    self.runner_tags,
                    self.project_id,
                    self.project_name,
                    self.merge_commit_message,
                    self.raw_event_id
                ),
            )
