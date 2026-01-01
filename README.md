# UAT Server Deployment Guide

This document contains step-by-step manual deployment instructions for the UAT environment.  
All commands must be executed on the server by a sudo-enabled user.

---

# 1. Set System Timezone

```bash
sudo timedatectl set-timezone Asia/Kolkata
sudo timedatectl
```

# 2. User Creation
```bash
sudo adduser biddbeuat
```

# 3. System Update & Basic Utilities
```bash
sudo apt update
sudo apt install -y curl net-tools
sudo apt install -y build-essential
sudo apt install -y python3 g++ make
sudo apt install -y bzip2
```

# 4. Mail Server (Postfix) Setup
## 4.1. Install Postfix & Mail Utilities
```bash
sudo apt install -y postfix mailutils
```
## 4.2. Enable & Verify Postfix

```bash
sudo systemctl enable postfix
sudo systemctl status postfix
```
## 4.3 Test Email
```bash
echo "This is a test mail" | mail -s "Test Email" your_email@example.com
mailq
sudo postqueue -f
```
# 5. Redis Installation (Local)

```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
redis-cli ping
```


# 6. Sudo Access Configuration
```bash
sudo visudo
```
Add
```bash
biddbeuat ALL=(ALL:ALL) ALL
```


# 7. Disk Setup & Home Directory Migration

## 7.1 Create GPT Partition

```bash
sudo parted /dev/nvme1n1 --script mklabel gpt
sudo parted /dev/nvme1n1 --script mkpart primary ext4 0% 100%
```

## 7.2 Format Disk

```bash
sudo mkfs.ext4 /dev/nvme1n1p1
```

## 7.3 Temporary Mount
```bash
sudo mount /dev/nvme1n1p1 /mnt
```

## 7.4 Backup Existing Home Directory
```bash
sudo rsync -av /home/biddfeprod/ /mnt/
```
## 7.5 Permanent Mount Configuration
```bash
echo '/dev/nvme1n1p1 /home/biddfeprod ext4 defaults 0 2' | sudo tee -a /etc/fstab
sudo umount /mnt
sudo mount -a
```

## 7.6 Verify Mount
```bash
df -h /home/biddfeprod
```

# 8. Node.js Setup Using NVM
```bash
sudo su - biddbeuat
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.nvm/nvm.sh
nvm --version
```

## 8.1 Install Node.js 20
```bash
nvm install 20
nvm use 20
nvm alias default 20
```

## 8.2 Install PM2
```bash
npm install -g pm2
exit

```
# 9. MongoDB 8.0 Installation
## 9.1 Add MongoDB Repository
```bash
curl -fsSL https://pgp.mongodb.com/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt update
```


## 9.2 Install & Enable MongoDB
```bash
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

## 9.3 Verify Versions

```bash
mongod --version
mongosh --version
```

# 10. MongoDB Atlas Connection
```bash
sudo su - biddbeuat
mongosh "mongodb+srv://biddEasyUat:******@biddeasyuat.itatx.mongodb.net/"

```

# 11. Java Installation
```bash
sudo apt install openjdk-17-jdk -y
java --version
```
# 12. Git Repository Configuration

```bash
git rm -r app.icm.communications
git submodule add -b main git@github.com:incredmoney/app.bidd.communications.git app.bidd.communications
```

# 13. AWS SES Configuration with Postfix
## 13.1 Disable Milters

```bash

sudo postconf -e "smtpd_milters="
sudo postconf -e "non_smtpd_milters="
sudo postconf -e "milter_default_action=accept"
sudo postconf -e "milter_protocol=6"

```

## 13.2 Restart Postfix

```bash

sudo systemctl restart postfix
sudo postconf -n | grep milter

```

## 13.3 SASL Authentication Setup
```bash
sudo mkdir -p /etc/postfix/sasl
sudo nano /etc/postfix/sasl/sasl_passwd
sudo postmap /etc/postfix/sasl/sasl_passwd
sudo chmod 600 /etc/postfix/sasl/sasl_passwd /etc/postfix/sasl/sasl_passwd.db
sudo chown root:root /etc/postfix/sasl/sasl_passwd*

```
# 14. External Service Networking

- SMS OTP & Hyperverge routed via proxy IP
- Proxy: oro db-nat – 10.0.1.166 (Oro AWS Account)

# 15. Swap Memory Configuration (4GB)
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

```
## 15.1 Optimize Swappiness
```bash
sudo sysctl vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swappiness.conf
```
# 16. Redis Decision (UAT)
AWS Redis currently disabled on UAT
Decision pending:
Use local Redis, OR
Migrate AWS Redis to new VPC if required

# 17. Application Certificates & Keys
Copy advisory certs into:
Incredmoney_api/certs
Copy jwtkeys folder into API repository

# 18. PM2 Startup Configuration

```bash
pm2 startup
```

Follow on-screen instructions to enable PM2 on boot.




