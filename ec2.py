def show_vpc_for_ec2():
    import boto3
    from botocore.exceptions import ClientError
    from config import AWS_REGION

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    try:
        vpcs_response = ec2_client.describe_vpcs()
        subnets_response = ec2_client.describe_subnets()

        all_subnets = subnets_response['Subnets']

        for vpc in vpcs_response['Vpcs']:
            vpc_id = vpc['VpcId']
            print(f"VPC ID: {vpc_id}")
            print(f"CIDR Block: {vpc['CidrBlock']}")
            print(f"Is Default: {vpc['IsDefault']}")
            print(f"State: {vpc['State']}")

            if 'Tags' in vpc:
                print("Tags:")
                for tag in vpc['Tags']:
                    print(f"  {tag['Key']}: {tag['Value']}")


            subnets_in_vpc = [s for s in all_subnets if s['VpcId'] == vpc_id]
            if subnets_in_vpc:
                print("Subnets:")
                for subnet in subnets_in_vpc:
                    print(f"  Subnet ID: {subnet['SubnetId']}")
                    print(f"  CIDR: {subnet['CidrBlock']}")
                    print(f"  Availability Zone: {subnet['AvailabilityZone']}")
                    print(f"  State: {subnet['State']}")
                    if 'Tags' in subnet:
                        print("   Tags:")
                        for tag in subnet['Tags']:
                            print(f"     {tag['Key']}: {tag['Value']}")
                    print("  -" * 10)
            else:
                print("No subnets found for this VPC.")

            print("=" * 40)

    except ClientError as e:
        print(f"Failed to describe VPCs or Subnets: {e}")

def create_security_group(description, name, vpc_id, cidr_ip):
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME
    # Create an EC2 client
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2_client.create_security_group(
        Description=description,
        GroupName=name,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {'Key': 'CreateBy', 'Value': CREATE_BY},
                    {'Key': 'Owner', 'Value': USERNAME}
                ]
            }
        ]
    )

    group_id = response['GroupId']

    ec2_client.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': cidr_ip,
                        'Description': 'SSH access',
                    },
                ],
                'ToPort': 22,
            },
        ],
    )
    return group_id


def ami_image(image_name):
    import boto3
    from config import AWS_REGION

    ssm = boto3.client('ssm', region_name=AWS_REGION)
    image_id_ubuntu = ssm.get_parameter(
        Name='/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id'
    )['Parameter']['Value']

    image_id_linux =  ssm.get_parameter(
        Name='/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64'
    )['Parameter']['Value']

    if image_name.lower() == 'ubuntu':
        return image_id_ubuntu
    elif image_name.lower() == 'amazon-linux':
        return image_id_linux
    else:
        print("only ubuntu or amazon linux!!")


def create_key(name_key):
    import boto3
    from botocore.exceptions import ClientError
    from config import AWS_REGION, CREATE_BY, USERNAME

    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    try:
        response = ec2.create_key_pair(
            KeyName=name_key,
            KeyType='rsa',
            KeyFormat='pem',
            TagSpecifications=[
                {
                    'ResourceType': 'key-pair',
                    'Tags': [
                        {'Key': 'CreateBy', 'Value': CREATE_BY},
                        {'Key': 'Owner', 'Value': USERNAME}
                    ]
                }
            ]
        )
        key_material = response['KeyMaterial']
        file_name = f"{name_key}.pem"
        with open(file_name, "w") as file:
            file.write(key_material)

        import os
        os.chmod(file_name, 0o400)


        print(f"Key pair '{name_key}' created successfully.")
        return response
    except ClientError as e:
        print(f"Failed to create key pair: {e}")
        return None

def delete_key(name_key):
    import boto3
    from config import AWS_REGION

    ec2 = boto3.client('ec2',region_name=AWS_REGION)
    response = ec2.delete_key_pair(KeyName=name_key)
    print(f"Key pair '{name_key}' deleted successfully.")

    import os

    file_name = f"{name_key}.pem"
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"Local key file '{file_name}' deleted.")
    else:
        print(f"Local key file '{file_name}' not found.")


def count_running_instances():
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:CreateBy', 'Values': [CREATE_BY]},
            {'Name': 'tag:Owner', 'Values': [USERNAME]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    count = 0
    for reservation in response['Reservations']:
        count += len(reservation['Instances'])

    return count






def create_ec2(instance_type, ami_image, instance_name, key_name, security_group_id,subnet_id):
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME
    from botocore.exceptions import ClientError



    if instance_type not in ['t3.micro', 't2.small']:
        print("Error: Instance type must be either 't3.micro' or 't2.small'.")
        return None

    running_count = count_running_instances()
    if running_count >= 2:
        print("Error: You have reached the limit of 2 running instances.")
        return None

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    try:
        instance = ec2_client.run_instances(
            ImageId=ami_image,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [

                            {'Key': 'Name', 'Value': instance_name},
                            {'Key': 'CreateBy', 'Value': CREATE_BY},
                            {'Key': 'Owner', 'Value': USERNAME}
                    ]
                }
            ]
        )

        instance_id = instance['Instances'][0]['InstanceId']
        print(f"Instance created: {instance_id}")
        return instance_id

    except ClientError as e:
        print(f"Failed to create EC2 instance: {e}")
        return None


def check_instance_tags(instance_id):
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    reservations = response.get('Reservations', [])
    if not reservations:
        print("Instance not found.")
        return False

    instance = reservations[0]['Instances'][0]
    tags = instance.get('Tags', [])

    tag_dict = {tag['Key']: tag['Value'] for tag in tags}
    if tag_dict.get('CreateBy') == CREATE_BY and tag_dict.get('Owner') == USERNAME:
        return True
    else:
        print("Access denied: instance is not created by you or your tool.")
        return False



def start_ec2(instance_id):
    import boto3
    from config import AWS_REGION
    from botocore.exceptions import ClientError

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    if not check_instance_tags(instance_id):
        return

    try:
        response = ec2_client.start_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )
        print(f"Start request sent for instance {instance_id}")
        return response

    except ClientError as e:
        print(f"Failed to start instance {instance_id}: {e}")




def stop_ec2(instance_id):
    import boto3
    from config import AWS_REGION
    from botocore.exceptions import ClientError

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    try:
        if not check_instance_tags(instance_id):
            return

        response =ec2_client.stop_instances(
            InstanceIds=[
                instance_id,
            ],
            Hibernate=False,
            SkipOsShutdown=False,
            DryRun=False,
            Force=False

        )

        print(f"Stop request sent for instance: {instance_id}")
        current_state = response['StoppingInstances'][0]['CurrentState']['Name']
        previous_state = response['StoppingInstances'][0]['PreviousState']['Name']
        print(f"Previous state: {previous_state} → Current state: {current_state}")
    except ClientError as e:
        print(f"Failed to start instance {instance_id}: {e}")

def list_instance():
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2_client.describe_instances(
        DryRun=False,
        Filters=[
            {'Name': 'tag:CreateBy', 'Values': [CREATE_BY]},
            {'Name': 'tag:Owner', 'Values': [USERNAME]}
        ],
        MaxResults=5
    )

    instances_info = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']


            name = "N/A"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break

            instance_data = {
                'InstanceId': instance_id,
                'Name': name,
                'State': state
            }

            instances_info.append(instance_data)


    for inst in instances_info:
        print(f"ID: {inst['InstanceId']} | Name: {inst['Name']} | State: {inst['State']}")

    return instances_info

def terminate_ec2(instance_id):
    import boto3
    from config import AWS_REGION
    from botocore.exceptions import ClientError

    ec2_client = boto3.client('ec2', region_name=AWS_REGION)

    if not check_instance_tags(instance_id):
        print("Access denied: instance is not created by you or your tool.")
        return

    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminate request sent for instance: {instance_id}")
        current_state = response['TerminatingInstances'][0]['CurrentState']['Name']
        previous_state = response['TerminatingInstances'][0]['PreviousState']['Name']
        print(f"Previous state: {previous_state} → Current state: {current_state}")
    except ClientError as e:
        print(f"Failed to terminate instance {instance_id}: {e}")

