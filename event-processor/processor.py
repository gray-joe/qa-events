from __future__ import annotations

import json
import os
from typing import Any

import psycopg2
from aws_lambda_typing import events, context as context_

from models.factories import JiraModelFactory, GitlabModelFactory


def process(event: events.SQSEvent, context: context_.Context) -> dict[str, Any]:
    """
    This is the intended entry point of the lambda.

    This lambda should process a given record in SQS and, if a message body is present it should treat it as a webhook.
    There are multiple pathways through this lambda to determine the source and type of event.

    :param event:
    :param context:
    :return:
    """
    message_body = event.get("Records", [{}])[0].get("body", False)
    if not message_body:
        print("No message body. Exiting...")
        return {
            "statusCode": 400,
            "body": "No event body found within the given message",
        }

    if process_event(json.loads(message_body)):
        print("Insert succeeded")
        return {"statusCode": 200, "body": "Event successfully written to the database"}
    else:
        print("Insert failed")
        return {"statusCode": 400, "body": "Event was not written to the database"}


def process_event(message_body: dict[str, Any]) -> dict[str, str | int] | bool:
    """
    Handles building models and routing different message bodies appropriately

    "workflow_job" signifies a GitHub workflow job event
    "check_request" signifies a GitHub workflow check event
    "pusher" signifies a GitHub push event
    "pusher_type" signifies a GitHub branch event
    "pull_request" signifies a GitHub pull request event
    "issue" signifies a GitHub issue event
    "object_kind" signifies any Gitlab event
    "issue_event_type_name" signifies any Jira event

    :param message_body:
    :return:
    """
    with psycopg2.connect(os.environ.get("POSTGRES_DSN")) as connection:
        with connection.cursor() as cursor:
            print("Attempting database insert")
            if "object_kind" in message_body:
                if "backfill" not in message_body:
                    inserted_id = write_raw_event_to_table(cursor, 'event', message_body)
                else:
                    print("Skipping raw event insert due to coming from a backfill job")
                    inserted_id = message_body['original_id']

                model = GitlabModelFactory.make(message_body, inserted_id)
            elif "issue_event_type_name" in message_body:
                if "backfill" not in message_body:
                    inserted_id = write_raw_event_to_table(cursor, 'jira_event', message_body)
                else:
                    print("Skipping raw event insert due to coming from a backfill job")
                    inserted_id = message_body['original_id']

                model = JiraModelFactory.make(message_body, inserted_id)
            else:
                return {"statusCode": 400, "body": "Nothing to write to database. Invalid webhook"}

            if model:
                model.save(connection)

    return inserted_id is not False


def write_raw_event_to_table(cursor, table: str, message_body: dict[str, Any]) -> int | bool:
    """
    Writes an event in its raw form straight to the event table which for gitlab is just known as event, but for
    Jira is known as jira_event

    We still want to maintain this functionality because it will enable us to do more bespoke queries
    if someone were to ask for them

    :param cursor:
    :param table:
    :param message_body:
    :return:
    """
    cursor.execute(
        """
        INSERT INTO {table}(data) VALUES(%s) RETURNING id
        """.format(table=table),
        (json.dumps(message_body),),
    )
    inserted_id = cursor.fetchone()[0]
    print(f"Inserted event. Returned ID: {inserted_id}")
    return inserted_id if cursor.rowcount == 1 else False
