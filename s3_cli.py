import click
from S3 import create_s3, upload_files, delete_bucket, list_buckets

@click.group(help="Manage S3 resources.")
def s3_cli():
    pass

@s3_cli.command(
    help="Create a new S3 bucket.",
    short_help="Create bucket"
)
@click.option('--name', required=True, help='Name of the bucket to create.')
@click.option(
    '--state', default='private', show_default=True,
    type=click.Choice(['private', 'public']),
    help='Bucket visibility (private or public).'
)
def create(name, state):
    create_s3(name, state)

@s3_cli.command(
    help="Upload a file to an existing S3 bucket.",
    short_help="Upload file"
)
@click.option('--file-name', required=True, help='Local file path to upload.')
@click.option('--bucket-name', required=True, help='Target S3 bucket name.')
@click.option('--key', required=True, help='Destination key (path) in the bucket.')
def upload(file_name, bucket_name, key):
    upload_files(file_name, bucket_name, key)

@s3_cli.command(
    help="List all buckets created by this CLI.",
    short_help="List buckets"
)
def list():
    list_buckets()

@s3_cli.command(
    help="Delete an S3 bucket (must be created by this CLI).",
    short_help="Delete bucket"
)
@click.option('--bucket-name', required=True, help='Name of the bucket to delete.')
def delete(bucket_name):
    delete_bucket(bucket_name)