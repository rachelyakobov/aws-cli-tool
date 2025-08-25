import click
from ec2_cli import ec2_cli
from s3_cli import s3_cli
from route53_cli import dns_cli

@click.group()
def cli():
    """Main CLI tool for managing AWS resources (EC2, S3, Route53)"""
    pass


cli.add_command(ec2_cli, name='ec2')
cli.add_command(s3_cli, name='s3')
cli.add_command(dns_cli, name='dns')

if __name__ == "__main__":
    cli()
