def r53_create_zones(name, vpc_id, state, comment= None):
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME
    import uuid
    from botocore.exceptions import ClientError

    route53_client = boto3.client('route53')
    state = state.lower()
    try:


        if state == 'private':
            response = route53_client.create_hosted_zone(
                Name=name,
                CallerReference=str(uuid.uuid4()),
                VPC={
                    'VPCRegion': AWS_REGION,
                    'VPCId': vpc_id,
                },
                HostedZoneConfig={
                    'Comment': comment,
                    'PrivateZone': True
                }
            )

        elif state == 'public':
            response = route53_client.create_hosted_zone(
                Name=name,
                CallerReference=str(uuid.uuid4()),
                HostedZoneConfig={
                    'Comment': comment,
                    'PrivateZone': False
                }
            )

        else:
            raise ValueError("State must be either 'public' or 'private'.")

        zone_id = response['HostedZone']['Id'].split('/')[-1]
        route53_client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=[
                {'Key': 'CreateBy', 'Value': CREATE_BY},
                {'Key': 'Owner', 'Value': USERNAME}
            ]
        )

        print(f"[SUCCESS] Hosted zone '{name}' created successfully. ID: {response['HostedZone']['Id']}")
        return response

    except route53_client.exceptions.HostedZoneAlreadyExists:
        print("Hosted zone already exists.")

    except route53_client.exceptions.InvalidDomainName:
        print(" Invalid domain name.")

    except route53_client.exceptions.TooManyHostedZones:
        print("Too many hosted zones in your account.")

    except route53_client.exceptions.InvalidInput as e:
        print("Invalid input:", e)

    except ClientError as e:
        print("AWS Client Error:", e)


def list_cli_hosted_zones():
    import boto3
    from config import CREATE_BY, USERNAME

    route53 = boto3.client('route53')
    zones = route53.list_hosted_zones()['HostedZones']
    cli_zones = []

    for zone in zones:
        zone_id = zone['Id'].split('/')[-1]
        tags_response = route53.list_tags_for_resource(ResourceType='hostedzone', ResourceId=zone_id)
        tags = tags_response.get('ResourceTagSet', {}).get('Tags', [])
        tags_dict = {tag['Key']: tag['Value'] for tag in tags}

        if tags_dict.get('CreateBy') == CREATE_BY and tags_dict.get('Owner') == USERNAME:
            cli_zones.append({
                'Id': zone_id,
                'Name': zone['Name']
            })

    return cli_zones


def manage_records(host_zone_id, action, domain_name, record_type, record_value, ttl=300 ):
    import boto3
    from config import AWS_REGION, CREATE_BY, USERNAME

    from botocore.exceptions import ClientError
    cli_zone_ids = [zone['Id'] for zone in list_cli_hosted_zones()]
    if host_zone_id not in cli_zone_ids:
        print(f"[ERROR] Hosted Zone '{host_zone_id}' is not owned by CLI. Action blocked.")
        return

    route53_client = boto3.client('route53')
    try:
        response = route53_client.change_resource_record_sets(
            HostedZoneId=host_zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': action.upper(),
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': record_type.upper() ,
                            'TTL': ttl,
                            'ResourceRecords': [{'Value': record_value}]
                        }
                    }
                ]
            }
        )
        print(f"[SUCCESS] Record {action.upper()} succeeded.")

    except ClientError as e:
        print(f"[ERROR] Failed to {action.upper()} record: {e}")


def list_records_for_zone(hosted_zone_id):
    import boto3

    route53 = boto3.client('route53')

    paginator = route53.get_paginator('list_resource_record_sets')
    records = []

    for page in paginator.paginate(HostedZoneId=hosted_zone_id):
        records.extend(page['ResourceRecordSets'])

    return records


def list_all_cli_records():
    cli_zones = list_cli_hosted_zones()

    for zone in cli_zones:
        print(f"\n Hosted Zone: {zone['Name']} (ID: {zone['Id']})")

        records = list_records_for_zone(zone['Id'])

        for record in records:
            name = record.get('Name')
            rtype = record.get('Type')
            ttl = record.get('TTL', '')


            values = []
            if 'ResourceRecords' in record:
                values = [r['Value'] for r in record['ResourceRecords']]
            elif 'AliasTarget' in record:
                values = [f"ALIAS -> {record['AliasTarget']['DNSName']}"]


            values_str = ', '.join(values) if values else '<no values>'
            print(f"  - {rtype:<6} {name:<40} TTL={str(ttl):<5} | {values_str}")

def delete_cli_hosted_zone(hosted_zone_id):
    import boto3
    from botocore.exceptions import ClientError

    route53 = boto3.client('route53')

    cli_zone_ids = [zone['Id'] for zone in list_cli_hosted_zones()]
    if hosted_zone_id not in cli_zone_ids:
        print(f"[ERROR] Hosted Zone '{hosted_zone_id}' is not owned by CLI. Deletion blocked.")
        return

    records = list_records_for_zone(hosted_zone_id)
    non_default_records = [
        r for r in records
        if r['Type'] not in ['NS', 'SOA']
    ]
    if non_default_records:
        print(f"[ERROR] Hosted Zone '{hosted_zone_id}' has non-default records. Please delete them first.")
        return

    try:
        route53.delete_hosted_zone(Id=hosted_zone_id)
        print(f"[SUCCESS] Hosted Zone '{hosted_zone_id}' deleted successfully.")
    except ClientError as e:
        print(f"[ERROR] Failed to delete hosted zone: {e}")


