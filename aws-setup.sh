#! /bin/sh
# Install Python, Docker, and Git
yum update -y
yum install git -y
amazon-linux-extras install python3
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
chkconfig docker on

# Install Docker Compose
curl -L https://github.com/docker/compose/releases/download/v2.12.1/docker-compose-linux-x86_64 | tee /usr/local/bin/docker-compose > /dev/null
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Pull the code from GitHub
cd /root
git clone https://github.com/id523a/NCARDDatabase.git
cd /root/NCARDDatabase
git checkout egiles_prod_ready

# Generate the secrets
cd /root/NCARDDatabase/NCARDDatabase/secrets
python3 gen_secrets.py

# Build the container
cd /root/NCARDDatabase
docker-compose build
