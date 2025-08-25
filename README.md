# platform-cli

`platform-cli` is a Python-based command-line interface for developers to self-manage AWS infrastructure within secure and standardized boundaries.

It supports the creation and management of:

- EC2 Instances
- S3 Buckets
- Route53 DNS Zones and Records

All resources are tagged to ensure that only CLI-created infrastructure is managed, avoiding accidental modification or deletion of unrelated AWS resources.

---

## Features

### EC2 Management

- Show available VPCs and subnets
- Retrieve latest AMI IDs (Amazon Linux / Ubuntu)
- Create and delete `.pem` SSH key pairs
- Create Security Groups with specific CIDR/IP rules
- Launch EC2 instances:
  - Supports instance types like `t3.micro` or `t2.small`
  - Allows configuration of key pair, security group, subnet
- Start, stop, and terminate EC2 instances
- List all instances created via this CLI

---

### S3 Bucket Management

- Create S3 buckets (private by default, optionally public)
- Upload files to existing buckets
- List all buckets created by this CLI
- Delete buckets created via CLI

---

### Route53 DNS Management

- Create Hosted Zones (public or private)
- List all hosted zones created via CLI
- Manage DNS records (create, update, delete)
  - Supports record types like `A`, `CNAME`, `TXT`
- View all DNS records in CLI-created zones
- Delete hosted zones (only if created by CLI)

---

## Tag-Based Ownership

Resources are tagged automatically using the following:

- `CreatedBy`
- `Owner`

These tags are used to:

- Ensure only CLI-managed resources can be listed, modified, or deleted
- Prevent accidental impact on existing production infrastructure

---
## To get started, please refer to the Prerequisites file
ן
