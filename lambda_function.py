import json
import boto3

def lambda_handler(event, context):
    """
    AWS Lambda handler that processes SQS messages containing
    email notification requests and sends them via Amazon SES.
    
    Expected SQS message body (JSON format):
    {
        "to": "recipient@example.com",
        "subject": "Email subject",
        "body": "Email body text"
    }
    """

    # Extract the raw body (string) from the first SQS record
    body_str = event['Records'][0]['body']
    print("Raw SQS message:", body_str)

    # Try to parse the body string as JSON into a Python dictionary
    try:
        sqs_message = json.loads(body_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return {"statusCode": 400, "body": "Invalid JSON"}

    # Extract the fields required for the email
    to_address = sqs_message.get("to")
    subject = sqs_message.get("subject", "CrediYa Notification")  # default subject
    body = sqs_message.get("body", "")  # default empty body

    print(f"Sending email to {to_address} with subject '{subject}'")

    # Create an Amazon SES client (region must be configured)
    ses_client = boto3.client("ses", region_name="us-east-2")

    # Send the email using SES
    response = ses_client.send_email(
        Source="email",  # must be a verified email/domain in SES
        Destination={"ToAddresses": [to_address]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {
                "Text": {"Data": body, "Charset": "UTF-8"}
            },
        },
    )

    print("SES response:", response)

    # Return a success response
    return {"statusCode": 200, "body": json.dumps("Email sent")}
