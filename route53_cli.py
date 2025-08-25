import click
from route53 import (
    r53_create_zones,
    list_cli_hosted_zones,
    manage_records,
    list_all_cli_records,
    delete_cli_hosted_zone
)

@click.group()
def dns_cli():
    """CLI tool for managing Route 53 zones and DNS records"""
    pass

@dns_cli.command()
@click.option('--name', required=True, help='Domain name (e.g., example.com)')
@click.option('--vpc-id', help='VPC ID (only for private zones)')
@click.option('--state', required=True, type=click.Choice(['public', 'private']), help='Zone type: public or private')
@click.option('--comment', default='', help='Optional comment')
def create_zone(name, vpc_id, state, comment):
    """Create a Route 53 hosted zone"""
    r53_create_zones(name, vpc_id, state, comment)


@dns_cli.command()
def list_zones():
    """List all CLI-created hosted zones"""
    zones = list_cli_hosted_zones()
    if not zones:
        print("No zones created by this CLI.")
    for zone in zones:
        print(f"Name: {zone['Name']} | ID: {zone['Id']}")


@dns_cli.command()
@click.option('--zone-id', required=True, help='Hosted zone ID')
@click.option('--action', required=True, type=click.Choice(['CREATE', 'DELETE', 'UPSERT']), help='Action type')
@click.option('--domain-name', required=True, help='Record domain name')
@click.option('--record-type', required=True, help='Record type (e.g., A, CNAME, TXT)')
@click.option('--record-value', required=True, help='Value of the record')
@click.option('--ttl', default=300, help='Time to live (TTL) in seconds')
def record(zone_id, action, domain_name, record_type, record_value, ttl):
    """Create, update, or delete a DNS record in a CLI-owned zone"""
    manage_records(zone_id, action, domain_name, record_type, record_value, ttl)


@dns_cli.command()
def list_records():
    """List all DNS records in CLI-created zones"""
    list_all_cli_records()

@dns_cli.command()
@click.option('--zone-id', required=True, help='Hosted zone ID to delete')
def delete_zone(zone_id):
    """Delete a hosted zone (must be CLI-created)"""
    delete_cli_hosted_zone(zone_id)