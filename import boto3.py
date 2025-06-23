import boto3
import os

def lambda_handler(event, context):
    # Get bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the file from S3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    text = response['Body'].read().decode('utf-8')
    
    # Count words
    word_count = len(text.split())
    
    # Prepare SNS message
    message = f"The word count in the {key} file is {word_count}."
    subject = "Word Count Result"
    
    # Publish to SNS
    sns = boto3.client('sns')
    topic_arn = "arn:aws:sns:us-west-2:705015544679:Lambda-challenge-sns"
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )
    
    return {
        'statusCode': 200,
        'body': message
    }