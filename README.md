# Cloud Kimaya — AWS Auto-Remediation Pipeline

## What this project does
Automatically detects errors in AWS CloudWatch logs and sends real-time alerts with smart recommendations to Slack — all within 60 seconds, zero human intervention.

## Architecture
CloudWatch Alarm → SNS Topic → Lambda Function → Slack Alert

## AWS Services Used
- CloudWatch — monitors log group for errors
- SNS — receives alarm and triggers Lambda
- Lambda — fetches logs and sends Slack alert
- S3 — stores logs
- IAM — manages permissions

## Features
- Real-time error detection
- Automatic Slack alerts
- Smart recommendations per error type
- Serverless architecture
- Free tier friendly

## Error Types Detected
- Database connection failures
- Memory exceptions
- Authentication failures
- Payment gateway timeouts
- Server down alerts
- File not found errors

## How to trigger a test alert
```bash
aws logs put-log-events \
  --log-group-name "/cloud-kimaya/app-logs" \
  --log-stream-name "test-stream" \
  --log-events timestamp=$(date +%s%3N),message="ERROR database connection failed" \
  --region us-east-1
```

## Resume Bullet Points
- Built serverless auto-remediation pipeline on AWS using CloudWatch, SNS and Lambda
- Automatically detects errors and sends Slack alerts with smart recommendations within 60 seconds
- Designed IAM security model with least-privilege roles for Lambda execution
