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
