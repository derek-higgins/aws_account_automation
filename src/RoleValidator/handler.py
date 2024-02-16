import json
import boto3

CHILD_ROLE="AccountAutomationRole"
def assume_role(account_id, role_name,service):
    sts_client =boto3.client('sts')
    
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AssumeRoleSession'
    )
    assumed_credentials=assumed_role['Credentials']
    
    client = boto3.client(
        service,
        aws_access_key_id=assumed_credentials['AccessKeyId'],
        aws_secret_access_key=assumed_credentials['SecretAccessKey'],
        aws_session_token=assumed_credentials['SessionToken']
    )
    return client
def handler(event, context):
    assume_role(event['accountId'])

    return {}