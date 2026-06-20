sudo apt install fontconfig openjdk-21-jre
sudo apt install jenkins
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc   https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]"   https://pkg.jenkins.io/debian-stable binary/ | sudo tee   /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
sudo ufw allow 8080/tcp
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
ssh-keygen -t rsa -b 4096
ssh-copy-id ash@192.168.1.202
ash@192.168.1.202
ssh ash@192.168.1.202
cat ~/.ssh/id_rsa
