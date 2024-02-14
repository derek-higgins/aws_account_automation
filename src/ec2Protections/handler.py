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

def enable_ec2_protections(account_id):
    ec2_client=assume_role(account_id=account_id,role_name=CHILD_ROLE,service='ec2')
    try:
        response = ec2_client.enable_ebs_encryption_by_default(DryRun=False)
        response = ec2_client.enable_image_block_public_access(ImageBlockPublicAccessState='block-new-sharing',DryRun=False)
        response=ec2_client.enable_snapshot_block_public_access(State='block-new-sharing', DryRun=False)
        return True
    except Exception as exp:
        print(f"erro: {exp}")
        return False
def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))
    enable_ec2_protections(event['accountId'])
    return {}