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
def apply_s3_public_block(account_id):
    s3_client=assume_role(account_id=account_id,role_name=CHILD_ROLE,service='s3control')
    try:
        response = s3_client.put_public_access_block(
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            },
            AccountId=account_id
        )
        return True
    except Exception as exp:
        print(f"erro: {exp}")
        return False
    
def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))
    apply_s3_public_block(event['accountId'])
    return {}