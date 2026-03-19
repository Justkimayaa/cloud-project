import json
import urllib.request
import os
import boto3

def get_recommendation(log_message):
    log_lower = log_message.lower()
    if 'database' in log_lower or 'connection' in log_lower:
        return "Check RDS instance status and verify security group rules"
    elif 'memory' in log_lower:
        return "Increase Lambda memory allocation or optimize code"
    elif 'authentication' in log_lower or 'auth' in log_lower:
        return "Check IAM roles and verify credentials are not expired"
    elif '404' in log_lower or 'not found' in log_lower:
        return "Check S3 bucket permissions and verify file path exists"
    elif 'timeout' in log_lower:
        return "Increase Lambda timeout or check network connectivity"
    elif 'payment' in log_lower:
        return "Check payment gateway API keys and network connectivity"
    elif 'server' in log_lower:
        return "Check EC2 instance health and restart if necessary"
    else:
        return "Check CloudWatch logs for more details and verify all services are running"

def lambda_handler(event, context):
    
    slack_webhook = os.environ['SLACK_WEBHOOK_URL']
    
    logs_client = boto3.client('logs')
    response = logs_client.get_log_events(
        logGroupName='/cloud-kimaya/app-logs',
        logStreamName='test-stream',
        limit=10
    )
    
    log_messages = [e['message'] for e in response['events']]
    logs_text = '\n'.join(log_messages)
    
    latest_log = log_messages[-1] if log_messages else "Unknown error"
    recommendation = get_recommendation(latest_log)
    
    slack_payload = json.dumps({
        "text": f":rotating_light: *AWS Alert*\n*Latest Logs:*\n```{logs_text}```\n:bulb: *Recommendation:* {recommendation}"
    }).encode()
    
    slack_req = urllib.request.Request(
        slack_webhook,
        data=slack_payload,
        headers={"Content-Type": "application/json"}
    )
    
    urllib.request.urlopen(slack_req)
    
    return {"statusCode": 200, "body": "Alert sent!"}
