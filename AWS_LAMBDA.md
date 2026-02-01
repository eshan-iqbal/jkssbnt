# AWS Lambda Deployment Guide

Deploy your JKSSB monitor as a serverless function on AWS Lambda with automatic scheduling.

## Architecture

```
EventBridge (Cron) → Lambda Function → JKSSB Website
                           ↓
                      DynamoDB (storage)
                           ↓
                    Telegram/Email/SNS
```

## Benefits

- ✅ **No server management** - Fully serverless
- ✅ **Cost-effective** - Pay only for execution time
- ✅ **Automatic scaling** - Handles any load
- ✅ **Reliable** - AWS infrastructure
- ✅ **Easy scheduling** - EventBridge cron expressions

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Basic knowledge of AWS services

## Step 1: Prepare Lambda Function

### Create Lambda Handler

Create `lambda_function.py`:

```python
import json
import os
import boto3
from monitor import JKSSBMonitor

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    
    # Override data file to use DynamoDB
    monitor = JKSSBMonitor()
    monitor.data_file = None  # We'll use DynamoDB instead
    
    # Fetch current notifications
    current_notifications = monitor.fetch_notifications()
    
    if not current_notifications:
        return {
            'statusCode': 200,
            'body': json.dumps('No notifications fetched')
        }
    
    # Get old notifications from DynamoDB
    try:
        response = table.get_item(Key={'id': 'latest'})
        old_notifications = response.get('Item', {}).get('notifications', [])
    except Exception as e:
        print(f"Error reading from DynamoDB: {e}")
        old_notifications = []
    
    # Find new notifications
    new_notifications = monitor.find_new_notifications(
        current_notifications,
        old_notifications
    )
    
    if new_notifications:
        # Send notifications
        monitor.send_notifications(new_notifications)
        
        # Save to DynamoDB
        try:
            table.put_item(
                Item={
                    'id': 'latest',
                    'notifications': current_notifications,
                    'updated_at': current_notifications[0].get('fetched_at')
                }
            )
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Found {len(new_notifications)} new notification(s)')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('No new notifications')
    }
```

### Create Deployment Package

```bash
# Create deployment directory
mkdir lambda-package
cd lambda-package

# Copy your code
cp ../monitor.py .
cp -r ../notifiers .
cp ../lambda_function.py .

# Install dependencies
pip install -r ../requirements.txt -t .

# Create ZIP file
zip -r ../jkssb-monitor-lambda.zip .
cd ..
```

## Step 2: Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name jkssb-notifications \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

## Step 3: Create IAM Role

Create `lambda-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the role:

```bash
aws iam create-role \
    --role-name jkssb-monitor-lambda-role \
    --assume-role-policy-document file://lambda-trust-policy.json
```

Attach policies:

```bash
# Basic Lambda execution
aws iam attach-role-policy \
    --role-name jkssb-monitor-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# DynamoDB access
aws iam attach-role-policy \
    --role-name jkssb-monitor-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

## Step 4: Create Lambda Function

```bash
aws lambda create-function \
    --function-name jkssb-monitor \
    --runtime python3.11 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/jkssb-monitor-lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://jkssb-monitor-lambda.zip \
    --timeout 60 \
    --memory-size 256 \
    --environment Variables="{
        DYNAMODB_TABLE=jkssb-notifications,
        TELEGRAM_BOT_TOKEN=your_token,
        TELEGRAM_CHAT_ID=your_chat_id
    }"
```

## Step 5: Create EventBridge Rule

Create a rule to run every 30 minutes:

```bash
aws events put-rule \
    --name jkssb-monitor-schedule \
    --schedule-expression "rate(30 minutes)"
```

Add Lambda permission:

```bash
aws lambda add-permission \
    --function-name jkssb-monitor \
    --statement-id jkssb-monitor-event \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:us-east-1:YOUR_ACCOUNT_ID:rule/jkssb-monitor-schedule
```

Add target:

```bash
aws events put-targets \
    --rule jkssb-monitor-schedule \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:jkssb-monitor"
```

## Step 6: Test

Test the function manually:

```bash
aws lambda invoke \
    --function-name jkssb-monitor \
    --payload '{}' \
    response.json

cat response.json
```

## Monitoring

View logs in CloudWatch:

```bash
aws logs tail /aws/lambda/jkssb-monitor --follow
```

## Cost Estimation

With checks every 30 minutes:
- **Lambda**: ~1,440 invocations/month × 1 second = ~$0.00
- **DynamoDB**: Minimal reads/writes = ~$0.00
- **EventBridge**: Free tier covers this
- **Total**: Essentially **FREE** (within free tier)

## Updating the Function

```bash
# Update code
cd lambda-package
zip -r ../jkssb-monitor-lambda.zip .
cd ..

# Upload new version
aws lambda update-function-code \
    --function-name jkssb-monitor \
    --zip-file fileb://jkssb-monitor-lambda.zip
```

## Environment Variables

Update environment variables:

```bash
aws lambda update-function-configuration \
    --function-name jkssb-monitor \
    --environment Variables="{
        DYNAMODB_TABLE=jkssb-notifications,
        TELEGRAM_BOT_TOKEN=new_token,
        TELEGRAM_CHAT_ID=new_chat_id,
        EMAIL_ENABLED=true,
        SMTP_USERNAME=email@example.com
    }"
```

## Terraform (Infrastructure as Code)

See `terraform/` directory for complete Terraform configuration to deploy everything automatically.

## Cleanup

To remove all resources:

```bash
# Delete EventBridge rule
aws events remove-targets --rule jkssb-monitor-schedule --ids 1
aws events delete-rule --name jkssb-monitor-schedule

# Delete Lambda function
aws lambda delete-function --function-name jkssb-monitor

# Delete DynamoDB table
aws dynamodb delete-table --table-name jkssb-notifications

# Delete IAM role
aws iam detach-role-policy --role-name jkssb-monitor-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam detach-role-policy --role-name jkssb-monitor-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
aws iam delete-role --role-name jkssb-monitor-lambda-role
```
