# UAT Server Deployment Guide

This document contains step-by-step manual deployment instructions for the UAT environment.  
All commands must be executed on the server by a sudo-enabled user.

---

## 1. Set System Timezone

```bash
sudo timedatectl set-timezone Asia/Kolkata
sudo timedatectl
```

## 2. User Creation
```bash
sudo adduser biddbeuat
```

## 3. System Update & Basic Utilities
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
## 5. Redis Installation (Local)

```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
redis-cli ping
```


## 6. Sudo Access Configuration
```bash
sudo visudo
```
Add
```bash
biddbeuat ALL=(ALL:ALL) ALL
```


# 7. Disk Setup & Home Directory Migration







# 5. Redis Installation (Local)



# 5. Redis Installation (Local)



# 5. Redis Installation (Local)



# 5. Redis Installation (Local)


