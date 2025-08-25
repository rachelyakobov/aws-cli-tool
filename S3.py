
def create_s3(bucket_name, state='private'):
    import boto3
    import botocore.exceptions
    from config import AWS_REGION, CREATE_BY, USERNAME

    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        create_bucket_params = {
            'Bucket': bucket_name,
        }

        if AWS_REGION != 'us-east-1':
            create_bucket_params['CreateBucketConfiguration'] = {
                'LocationConstraint': AWS_REGION
            }

        s3_client.create_bucket(**create_bucket_params)

        s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {'Key': 'CreateBy', 'Value': CREATE_BY},
                    {'Key': 'Owner', 'Value': USERNAME}
                ]
            }
        )

        if state == 'public':
            s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )

        print(f"S3 bucket '{bucket_name}' created as {state}.")
        return True

    except botocore.exceptions.ClientError as e:
        print(f"Error creating S3 bucket: {e}")
        return False

def upload_files(file_name, bucket_name, key):
    import boto3
    from botocore.exceptions import ClientError
    from config import AWS_REGION, CREATE_BY, USERNAME

    s3_client = boto3.client('s3', region_name=AWS_REGION)

    try:
        tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag['Key']: tag['Value'] for tag in tagging['TagSet']}
    except ClientError as e:
        print(f"Unable to access tags for bucket '{bucket_name}':", e)
        return False

    if tags.get("CreateBy") != CREATE_BY or tags.get("Owner") != USERNAME:
        print(f"Upload not allowed – bucket '{bucket_name}' does not match required tags.")
        return False

    try:
        s3_client.upload_file(file_name, bucket_name, key)
        print(f"File '{file_name}' uploaded to '{bucket_name}/{key}'")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False

def list_buckets():
    import boto3
    from botocore.exceptions import ClientError
    from config import AWS_REGION, CREATE_BY, USERNAME

    s3_client = boto3.client('s3', region_name=AWS_REGION)

    response = s3_client.list_buckets()
    buckets = response['Buckets']

    buckets_with_tag = []

    for bucket in buckets:
        bucket_name = bucket['Name']

        try:
            tags_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
            tags = {tag['Key']: tag['Value'] for tag in tags_response.get('TagSet', [])}

            if tags.get('CreateBy') == CREATE_BY and tags.get('Owner') == USERNAME:
                buckets_with_tag.append(bucket_name)

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                pass


    print("S3 buckets created by cli-tool:", buckets_with_tag)
    return buckets_with_tag


def delete_bucket(bucket_name):
    import boto3
    from botocore.exceptions import ClientError
    from config import AWS_REGION, CREATE_BY, USERNAME

    s3_client = boto3.client('s3', region_name=AWS_REGION)
    s3_resource = boto3.resource('s3', region_name=AWS_REGION)
    bucket = s3_resource.Bucket(bucket_name)


    try:
        tags_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag['Key']: tag['Value'] for tag in tags_response.get('TagSet', [])}
    except ClientError as e:
        print(f"Cannot get tags for bucket '{bucket_name}': {e}")
        return

    if tags.get('CreateBy') == CREATE_BY and tags.get('Owner') == USERNAME:
        try:

            bucket.objects.all().delete()

            s3_client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted successfully.")

        except ClientError as e:
            print(f"Failed to delete bucket '{bucket_name}': {e}")
    else:
        print(f"Bucket '{bucket_name}' does not belong to you. Skipping deletion.")






