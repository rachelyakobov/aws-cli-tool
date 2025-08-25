# Usage Examples

All commands follow this format:

aws-cli <resource> <action> [parameters] ---> with alias
or
python3 main_cli.py <resource> <action> [parameters] 

### HELP
python3 main_cli.py --help or aws-cli --help

<img width="879" height="290" alt="image" src="https://github.com/user-attachments/assets/3e0c04e9-8fe7-44b7-85dc-04d0dd28a91b" />



### Create EC2 instance

aws-cli ec2 create-instance --instance-type t3.micro --ami-image ami-xxxxxxx --instance-name my-instance --key-name my-key --security-group-id sg-xxxxxxx --subnet-id subnet-xxxxxxx

If you don't have an AMI image ID, key pair, or security group, you can create them first with the CLI commands below.

#### Create a key pair
aws-cli ec2 create-key-pair --key-name my-key

#### Create a security group
aws-cli ec2 create-sg --description "My security group" --name my-sg --vpc-id vpc-xxxxxxx --cidr-ip 0.0.0.0/0

#### Find an AMI image by name
aws-cli ec2 ami --image-name ubuntu
 
### List instances
aws-cli ec2 list-instances

### Start instance
aws-cli ec2 start --instance-id i-1234567890

### Stop instance
aws-cli ec2 stop --instance-id i-1234567890

### Terminate instance
aws-cli ec2 Terminate --instance-id i-1234567890

### Help ec2
python3 main_cli.py ec2 --help aws-cli ec2 --help

python3 main_cli.py create-instance --help aws-cli ec2 create-instance --help


###  Create a Bucket

Private (default):  

aws-cli s3 create --name my-private-bucket

Public:  

aws-cli s3 create --name my-public-bucket --state public

---

### Upload a File to a Bucket

aws-cli s3 upload --file-name ./myfile.txt --bucket-name my-private-bucket --key documents/myfile.txt

---

### List Buckets Created by This CLI

aws-cli s3 list

---

### Delete a Bucket

aws-cli s3 delete --bucket-name my-private-bucket

---

## Help s3
python3 main_cli.py s3 --help or aws-cli s3 --help  

python3 main_cli.py s3 create --help or aws-cli s3 create --help

---

### Create a Hosted Zone

Public zone:  
aws-cli dns create-zone --name example.com --state public

Private zone (with VPC):  
aws-cli dns create-zone --name example.com --state private --vpc-id vpc-xxxxxxxx

---

### List Hosted Zones

aws-cli dns list-zones

---

### Add a DNS Record

aws-cli dns record --zone-id ZONEID --action CREATE --domain-name www.example.com --record-type A --record-value 1.2.3.4

---

### Update a DNS Record

aws-cli dns record --zone-id ZONEID --action UPSERT --domain-name www.example.com --record-type A --record-value 5.6.7.8

---

### Delete a DNS Record

aws-cli dns record --zone-id ZONEID --action DELETE --domain-name www.example.com --record-type A --record-value 5.6.7.8

---

### List All Records in All Zones

aws-cli dns list-records

---

### Delete a Hosted Zone

aws-cli dns delete-zone --zone-id ZONEID

---

## Help dns
python3 main_cli.py dns --help or aws-cli dns  --help  

python3 main_cli.py dns create --help or aws-cli dns delete-zone --help

