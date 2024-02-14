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

def remove_default_vpc(account_id):
    ec2 = assume_role(account_id=account_id,role_name=CHILD_ROLE,service='ec2')

    # Get information about all VPCs
    response = ec2.describe_vpcs()

    # Find the default VPC
    default_vpcs = [vpc['VpcId'] for vpc in response['Vpcs'] if vpc['IsDefault']]

    if not default_vpcs:
        print("Default VPC not found.")
        return

    default_vpc_id = default_vpcs[0]
    print(f"Default VPC found with ID: {default_vpc_id}")

    # Delete all resources associated with the default VPC
        # Delete default subnets

    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [default_vpc_id]}])
    for subnet in response['Subnets']:
        try:
            ec2.delete_subnet(SubnetId=subnet['SubnetId'])
            print(f"Deleted subnet: {subnet['SubnetId']}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
        # Delete default security groups
      
        response = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [default_vpc_id]}])
        for security_group in response['SecurityGroups']:
            try:
                ec2.delete_security_group(GroupId=security_group['GroupId'])
                print(f"Deleted security group: {security_group['GroupId']}")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Detach and delete internet gateway
        response = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id', 'Values': [default_vpc_id]}])
        for igw in response['InternetGateways']:
            try:
                ec2.detach_internet_gateway(InternetGatewayId=igw['InternetGatewayId'], VpcId=default_vpc_id)
                ec2.delete_internet_gateway(InternetGatewayId=igw['InternetGatewayId'])
                print(f"Detached and deleted Internet Gateway: {igw['InternetGatewayId']}")
            except Exception as e:
                print(f"An error occurred: {e}")
        # Delete default VPC
        try:
            ec2.delete_vpc(VpcId=default_vpc_id)
            print(f"Deleted default VPC: {default_vpc_id}")
        except Exception as e:
            print(f"An error occurred: {e}")
        print("Default VPC and associated resources removed successfully.")

def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))
    remove_default_vpc(event['accountId'])

    return {}