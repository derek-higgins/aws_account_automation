import json
import boto3

CHILD_ROLE="AccountAutomationRole"
def get_regions():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions

def assume_role(account_id, role_name,service, region="us-east-1"):
    sts_client =boto3.client('sts')
    
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AccountAutomation'
    )
    assumed_credentials=assumed_role['Credentials']
    
    client = boto3.client(
        service,
        aws_access_key_id=assumed_credentials['AccessKeyId'],
        aws_secret_access_key=assumed_credentials['SecretAccessKey'],
        aws_session_token=assumed_credentials['SessionToken'],
        region_name=region
    )
    return client


def enable_ec2_protections(account_id,region_name):
    ec2_client=assume_role(account_id=account_id,role_name=CHILD_ROLE,service='ec2',region=region_name)
    try:
        response = ec2_client.enable_ebs_encryption_by_default(DryRun=False)
        response = ec2_client.enable_image_block_public_access(ImageBlockPublicAccessState='block-new-sharing',DryRun=False)
        response=ec2_client.enable_snapshot_block_public_access(State='block-new-sharing', DryRun=False)
        return True
    except Exception as exp:
        print(f"erro: {exp}")
        return False
def handler(event, context):
    for region in get_regions():
        enable_ec2_protections(event['accountId'], region)

    return {}