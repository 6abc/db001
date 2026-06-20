# Jenkins Installation and SSH Setup Guide

## Prerequisites

Install Java 21 and font support:

```bash
sudo apt install fontconfig openjdk-21-jre
```

---

## Add Jenkins Repository

Download the Jenkins repository key:

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
```

Add the Jenkins repository:

```bash
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Update package information:

```bash
sudo apt update
```

---

## Install Jenkins

Install Jenkins:

```bash
sudo apt install jenkins
```

Enable Jenkins to start automatically:

```bash
sudo systemctl enable jenkins
```

Start the Jenkins service:

```bash
sudo systemctl start jenkins
```

Check the service status:

```bash
sudo systemctl status jenkins
```

---

## Configure Firewall

Allow access to Jenkins on port **8080**:

```bash
sudo ufw allow 8080/tcp
```

---

## Get Initial Admin Password

Retrieve the Jenkins initial admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Use this password to complete the setup at:

```
http://<server-ip>:8080
```

---

# SSH Key Setup

## Generate an SSH Key Pair

Create a 4096-bit RSA key:

```bash
ssh-keygen -t rsa -b 4096
```

---

## Copy Public Key to Remote Server

Copy your SSH key to the remote machine:

```bash
ssh-copy-id ash@192.168.1.202
```

---

## Connect to Remote Server

Log in to the server:

```bash
ssh ash@192.168.1.202
```

---

## View Private Key

Display your private key:

```bash
cat ~/.ssh/id_rsa
```

> ⚠️ **Security Warning**
>
> Never share or expose your private key (`id_rsa`). Only the public key (`id_rsa.pub`) should be shared.

---

## Summary

| Task                   | Command                                                  |
| ---------------------- | -------------------------------------------------------- |
| Install Java           | `sudo apt install fontconfig openjdk-21-jre`             |
| Add Jenkins Repository | `wget ...jenkins.io-2026.key`                            |
| Update Packages        | `sudo apt update`                                        |
| Install Jenkins        | `sudo apt install jenkins`                               |
| Start Jenkins          | `sudo systemctl start jenkins`                           |
| Enable Auto Start      | `sudo systemctl enable jenkins`                          |
| Check Status           | `sudo systemctl status jenkins`                          |
| Allow Port 8080        | `sudo ufw allow 8080/tcp`                                |
| Get Admin Password     | `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` |
| Generate SSH Key       | `ssh-keygen -t rsa -b 4096`                              |
| Copy Key to Server     | `ssh-copy-id ash@192.168.1.202`                          |
| Connect to Server      | `ssh ash@192.168.1.202`                                  |
