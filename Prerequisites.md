# Setup and Installation Guide

Before running this CLI tool, make sure your environment is set up with Python 3, AWS CLI, and required Python packages. Also, configure your AWS credentials.

---

# Installation Steps

## For Amazon Linux / CentOS / RHEL (using yum)

sudo yum update -y  

sudo yum install python3 pip -y

### Verify installations
python3 --version

pip3 --version

### Install AWS CLI-
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscli.zip"

unzip awscli.zip

sudo ./aws/install

### Verify AWS CLI
aws --version

### Configure AWS credentials
aws configure

### Clone the repository and enter the project directory
git clone https://github.com/rachelyakobov/aws-cli-tool.git

cd aws-cli-tool



### Install Python dependencies
pip3 install -r requirements.txt

## For Ubuntu / Debian (using apt)
sudo apt update && sudo apt upgrade -y

sudo apt install python3 python3-pip unzip curl -y

### Verify installations
python3 --version

pip3 --version

### Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscli.zip"

unzip awscli.zip

sudo ./aws/install

### Verify AWS CLI
aws --version

### Configure AWS credentials - put your Access key and Secret access key
aws configure

### Clone the repository and enter the project directory
git clone https://github.com/rachelyakobov/aws-cli-tool.git

cd aws-cli-tool


### Install Python dependencies
pip3 install -r requirements.txt

---
# Edit `config.py` to add your credentials

### Edit `config.py` to add your credentials

Use `vim` (or any other text editor) to open the `config.py` file and fill in the required details, such as AWS access keys, regions, etc.

vim config.py


<img width="803" height="89" alt="image" src="https://github.com/user-attachments/assets/cd66e0d9-4aad-4c21-be3e-f24e697169cd" />


# Creating a command alias

To simplify running the CLI tool, add an alias:

echo 'alias aws-tool="python3 /path/to/your/project/main_cli.py"' >> ~/.bashrc

source ~/.bashrc

# To see usage examples of the CLI tool, go to the examples file



