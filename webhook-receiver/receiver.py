import json
from typing import Any
import boto3
from botocore.exceptions import ClientError

sqs = boto3.client("sqs")
aws_account_id = boto3.client("sts").get_caller_identity().get("Account")


def remove_description_from_message(message_body: dict) -> dict[str, Any]:
    """
    Remove the description from the message body of PR events to ensure the payload
    remains under the 256kb limit.

    :param message_body: A JSON object received from the webhook
    :return:
    """
    if 'pull_request' in message_body and 'body' in message_body.get('pull_request'):
        message_body['pull_request']['body'] = ''
    return message_body


def put_event_in_queue(message_body: str) -> None:
    """
    Places an event on to the `qh-events-webhook-processor-queue` SQS queue

    :param message_body: A raw JSON object received from the webhook
    :return:
    """
    message_body = remove_description_from_message(message_body)
    try:
        sqs.send_message(
            QueueUrl=f"https://sqs.eu-west-2.amazonaws.com/{aws_account_id}/qh-events-webhook-processor-queue",
            MessageBody=message_body,
        )
    except ClientError as error:
        print(f"Adding an event to the queue has failed. Original event: {message_body}")
        raise error


def lambda_handler(event, context) -> dict[str, Any]:
    """
    Lambda entry point, takes a raw event from webhooks and places them directly on to an SQS queue

    :param event: The event forwarded to the lambda from the API Gateway endpoint
    :param context: Irrelevant as we do not have multiple contexts to handle
    :return: A dictionary containing a HTTP status code and an associated message depending on success
    """
    print("Webhook received")
    event_type = event.get("headers", {}).get("x-github-event")
    message_time = event.get("requestContext", {}).get("timeEpoch")
    message_body = event.get("body")

    if message_body == None:
        print("Webhook contained no message body. Exiting")
        return {
            "statusCode": 400,
            "body": "The given event does not contain a body to be parsed.",
        }

    try:
        print("Placing webhook data into the queue")
        put_event_in_queue(message_body)
    except ClientError as error:
        print("Could not point the webhook into the queue")
        print(error)
        return {
            "statusCode": 400,
            "body": "An error was encountered when adding an item to the queue",
        }

    print("Successfully added the webhook to the queue")
    return {"statusCode": 200, "body": "Successfully added webhook event to the queue"}