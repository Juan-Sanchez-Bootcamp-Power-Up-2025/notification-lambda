import json
import boto3

def notification_handler(event, context):
    # body as string
    body_str = event['Records'][0]['body']
    print("Raw SQS message:", body_str)

    # pars to dict
    try:
        sqs_message = json.loads(body_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return {"statusCode": 400, "body": "Invalid JSON"}

    # gets the notification fields
    to_address = sqs_message.get("to")
    subject = sqs_message.get("subject", "CrediYa Notification")
    body = sqs_message.get("body", "")

    print(f"Sending email to {to_address} with subject '{subject}'")

    # SES Client
    ses_client = boto3.client("ses", region_name="us-east-2")

    # Sends email
    response = ses_client.send_email(
        Source="email",  # must be verified on SES
        Destination={"ToAddresses": [to_address]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Text": {"Data": body, "Charset": "UTF-8"}},
        },
    )

    print("SES response:", response)
    return {"statusCode": 200, "body": json.dumps("Email sent")}
