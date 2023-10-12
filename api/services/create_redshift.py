
S3_ACCESS_KEY = 'AKIARGBJ7XJP3EFM42GS'

S3_SECRET_KEY = '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'

vpc_id='vpc-0024921d5098938f8'
from botocore.exceptions import ClientError
import boto3
#create security group
ec2_client = boto3.client('ec2', 
                          aws_access_key_id='AKIA3OBOBB2KAPCAI5EE', 
                          aws_secret_access_key= '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',region_name="ap-south-1")

group_name = 'my-redshift-security-group'
group_description = 'Security group for Redshift cluster access'




try:
    # Create the security group
    response = ec2_client.create_security_group(
        GroupName=group_name,
        Description=group_description,
        VpcId=vpc_id
    )
    security_group_id = response['GroupId']
    print('Created security group with ID:', security_group_id)
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
        # The security group already exists
        response = ec2_client.describe_security_groups(
            Filters=[
                {'Name': 'group-name', 'Values': [group_name]},
                {'Name': 'vpc-id', 'Values': [vpc_id]}
            ]
        )
        security_group_id = response['SecurityGroups'][0]['GroupId']
        print('Security group already exists. Using existing security group with ID:', security_group_id)
    else:
        # Handle other exceptions
        print('Error creating security group:', e)


