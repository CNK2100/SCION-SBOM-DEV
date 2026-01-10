# SCION-SBOM-DEV
Development of SBOM on SCION

## Hardware details
- OS: Installation on Ubuntu 22.04 Laptop.
- CPU arch: AMD64. We did not tested on Arm cpu such as Apple Silicon.
- CPU Hardware: Intel Core i7.
- 16 GB of RAM.

## Ubuntu 22.04 update
```
sudo apt update
sudo apt upgrade

```

## SCION INSTALLATION
### Requirements

```
sudo apt install wget
sudo apt-get install -y graphviz
sudo apt install golang-go
go version
sudo apt install default-jdk
sudo apt install locate
updatedb
```
Installation of Docker
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo apt-get install docker-compose-plugin
sudo systemctl status docker
sudo apt-get update
sudo groupadd docker
sudo usermod -aG docker $USER
sudo usermod -aG docker #YourUsername
newgrp docker
groups
```
Close the terminal and open it again
Groups  // verify if your username is in docker or restart your computer to take effect.
If not add again below commands

```
sudo usermod -aG docker #YourUsername
newgrp docker
groups
```
Running initial docker instance
```
sudo systemctl status docker
docker run hello-world     ## wait for docker to download the hello prg


```

## SCION QUANTUM INSTALLATION
### Requirements
Install all above SCION depencies if not installed and proceed.

```

```



