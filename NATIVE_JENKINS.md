# Jenkins Installation and Remote Node Setup Guide

## Prerequisites

Install Java:

```bash
sudo apt install fontconfig openjdk-21-jre
```

---

# Install Jenkins

## Add Jenkins Repository Key

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
```

## Add Repository

```bash
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Update packages:

```bash
sudo apt update
```

Install Jenkins:

```bash
sudo apt install jenkins
```

Enable and start Jenkins:

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

Check status:

```bash
sudo systemctl status jenkins
```

Allow port 8080:

```bash
sudo ufw allow 8080/tcp
```

Get initial admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open:

```
http://<JENKINS_SERVER_IP>:8080
```

Complete the Jenkins setup wizard.

---

# Configure SSH Keys

## Generate SSH Key

On the Jenkins server:

```bash
ssh-keygen -t rsa -b 4096
```

Press Enter to accept defaults.

---

## Display Public Key

```bash
cat ~/.ssh/id_rsa.pub
```

Example:

```text
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ... user@hostname
```

Copy the entire output.

---

## Add Public Key to Remote Machine

### Method 1 (Recommended)

```bash
ssh-copy-id ash@192.168.1.202
```

### Method 2 (Manual)

SSH into the remote machine:

```bash
ssh ash@192.168.1.202
```

Create `.ssh` directory if needed:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Edit authorized_keys:

```bash
nano ~/.ssh/authorized_keys
```

Paste the contents of:

```bash
cat ~/.ssh/id_rsa.pub
```

Save and exit.

Set permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

---

## Verify Passwordless Login

From Jenkins server:

```bash
ssh ash@192.168.1.202
```

Login should occur without asking for a password.

---

# Add Remote Node (Agent) in Jenkins

## Step 1: Open Jenkins Dashboard

Navigate to:

```
Manage Jenkins
    ↓
Nodes
    ↓
New Node
```

---

## Step 2: Create Node

Node name:

```
agent1
```

Select:

```
Permanent Agent
```

Click **Create**.

---

## Step 3: Configure Agent

### Number of executors

```
1
```

### Remote root directory

Example:

```
/home/ash/jenkins-agent
```

Create directory on remote machine:

```bash
ssh ash@192.168.1.202

mkdir -p ~/jenkins-agent
```

### Labels

```
linux
```

### Usage

```
Use this node as much as possible
```

### Launch method

Choose:

```
Launch agents via SSH
```

---

## Step 4: Configure SSH Connection

Host:

```
192.168.1.202
```

Credentials:

```
Add → Jenkins
```

Kind:

```
SSH Username with private key
```

Username:

```
ash
```

Private Key:

```
Enter directly
```

Paste contents of:

```bash
cat ~/.ssh/id_rsa
```

(From the Jenkins server)

ID:

```
agent1-key
```

Description:

```
SSH key for agent1
```

Click **Add**.

---

## Step 5: Save

Click:

```
Save
```

Jenkins will connect to the remote machine and install the agent automatically.

---

# Verify Agent

Go to:

```
Dashboard
    ↓
Nodes
```

The node should display:

```
agent1
Status: Connected
```

---

# Test

Pipeline example:

```groovy
pipeline {
    agent {
        label 'linux'
    }

    stages {
        stage('Test') {
            steps {
                sh 'hostname'
                sh 'whoami'
                sh 'java -version'
            }
        }
    }
}
```

This confirms that builds are running on the remote agent.
