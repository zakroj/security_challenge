import boto3
import logging
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    if event.get('action') == 'create':
        return create_bucket(event.get('bucket_name'))
    elif event.get('action') == 'delete':
        return delete_bucket(event.get('bucket_name'))
    elif event.get('action') == 'list':
        return list_bucket()

def create_bucket(bucket_name, region='eu-central-1'):
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return {
            'statusCode': 200,
            'body': {
                'error': e
            }
        }
    return {
            'statusCode': 200,
            'body': {
                'response': 'successfull'
            }
        }

def list_bucket():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f' {bucket["Name"]}')
    
    return {
            'statusCode': 200,
            'body': {
                'response': 'buckets listed successfully'
            }
        }

def delete_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        # Delete the S3 bucket
        s3.delete_bucket(Bucket=bucket_name)

        # Return a success message
        return {
            'statusCode': 200,
            'body': f'S3 bucket "{bucket_name}" deleted successfully'
        }
    except ClientError as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': {
                'error': e
            }
        }