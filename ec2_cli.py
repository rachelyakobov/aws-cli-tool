import click
from ec2 import (
    show_vpc_for_ec2,
    ami_image,
    create_key,
    delete_key,
    create_ec2,
    create_security_group,
    stop_ec2,
    start_ec2,
    list_instance,
    terminate_ec2
)

@click.group()
def ec2_cli():
    """EC2 Management Tool"""
    pass

@ec2_cli.command()
def show_vpcs():
    """Show VPCs and Subnets"""
    show_vpc_for_ec2()

@ec2_cli.command()
@click.option('--description', prompt='Description', help='Security group description')
@click.option('--name', prompt='Name', help='Security group name')
@click.option('--vpc-id', prompt='VPC ID', help='VPC ID')
@click.option('--cidr-ip', prompt='CIDR IP', help='CIDR IP for SSH access')
def create_sg(description, name, vpc_id, cidr_ip):
    """Create a new Security Group"""
    sg_id = create_security_group(description, name, vpc_id, cidr_ip)
    click.echo(f"Security Group created with ID: {sg_id}")

@ec2_cli.command()
@click.option('--image-name', prompt='Image name', help='AMI Image name (ubuntu/amazon linux)')
def ami(image_name):
    """Get AMI by name"""
    ami_id = ami_image(image_name)
    click.echo(f"AMI ID for {image_name}: {ami_id}")

@ec2_cli.command()
@click.option('--key-name', prompt='Key pair name', help='Key pair name')
def create_key_pair(key_name):
    """Create a new Key Pair"""
    create_key(key_name)

@ec2_cli.command()
@click.option('--key-name', prompt='Key pair name', help='Key pair name to delete')
def delete_key_pair(key_name):
    """Delete a Key Pair"""
    delete_key(key_name)

@ec2_cli.command()
@click.option('--instance-type', prompt='Instance type', help='Instance type (t3.micro or t2.small)')
@click.option('--ami-image', prompt='AMI image', help='AMI Image ID')
@click.option('--instance-name', prompt='Instance name', help='Name tag for the instance')
@click.option('--key-name', prompt='Key pair name', help='Key pair name')
@click.option('--security-group-id', prompt='Security Group ID', help='Security Group ID')
@click.option('--subnet-id', prompt='Subnet ID', help='Subnet ID')
def create_instance(instance_type, ami_image, instance_name, key_name, security_group_id, subnet_id):
    """Create a new EC2 instance"""
    instance_id = create_ec2(instance_type, ami_image, instance_name, key_name, security_group_id, subnet_id)
    if instance_id:
        click.echo(f"Created instance: {instance_id}")

@ec2_cli.command()
@click.option('--instance-id', prompt='Instance ID', help='Instance ID to start')
def start(instance_id):
    """Start an EC2 instance"""
    start_ec2(instance_id)

@ec2_cli.command()
@click.option('--instance-id', prompt='Instance ID', help='Instance ID to stop')
def stop(instance_id):
    """Stop an EC2 instance"""
    stop_ec2(instance_id)

@ec2_cli.command()
def list_instances():
    """List EC2 instances"""
    list_instance()

@ec2_cli.command()
@click.option('--instance-id', prompt='Instance ID', help='Instance ID to terminate')
def terminate(instance_id):
    """Terminate an EC2 instance"""
    terminate_ec2(instance_id)


