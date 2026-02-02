# SCION-SBOM-DEV
The implementation of RBOM into SCION infrastructure.
The code is based on [the SCION implementation](https://github.com/netsec-ethz/scion).

## Installation 

Installation packages for Debian and derivatives are available for x86-64, arm64, x86-32 and arm.
These packages can be found in the [latest release](https://github.com/scionproto/scion/releases/latest).
Packages for in-development versions can be found from the [latest nightly build](https://buildkite.com/scionproto/scion-nightly/builds/latest).

Alternatively, "naked" pre-built binaries are available for Linux x86-64 and
can be downloaded from the [latest release](https://github.com/scionproto/scion/releases/latest) or the
[latest nightly build](https://buildkite.com/scionproto/scion-nightly/builds/latest).

[SCION-SBOM forked  from Quantum](https://github.com/juagargi/quantum.git).

## Hardware details
- OS: Installation on Ubuntu 22.04 Laptop.
- CPU arch: AMD64. We did not tested on Arm cpu such as Apple Silicon.
- CPU Hardware: Intel Core i7.
- RAM: 16 GB.
- DISK: 256 GB

## Ubuntu 22.04 update
```
owner@owner:~/quantum$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.5 LTS
Release:	22.04
Codename:	jammy
owner@owner:~/quantum$ 
```
Update & upgrade
```
sudo apt update
sudo apt upgrade

```


### Requirements

```
sudo apt update
sudo apt upgrade

sudo apt install wget
sudo apt install golang-go
go version

sudo apt install default-jdk
sudo apt install locate
updatedb

sudo apt-get install -y graphviz python3-graphviz
pip install pyyaml toml plumbum 
sudo apt install -y clang llvm libbpf-dev linux-headers-$(uname -r)
sudo apt-get install -y linux-headers-$(uname -r) clang llvm libbpf-dev libelf-dev
sudo apt install -y linux-tools-common linux-tools-$(uname -r)
bpftool version

sudo apt-get install -y build-essential cmake git pkg-config libssl-dev ninja-build
sudo apt-get install -y supervisor

```
### Docker
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo apt-get install docker-compose-plugin
sudo systemctl status docker
sudo apt-get update
sudo groupadd docker
# Add your user to docker group
sudo usermod -aG docker $USER
sudo usermod -aG docker #YourUsername
# Verify it's added to system
getent group docker
# Update the configuration
newgrp docker
groups
```
Close the terminal and open it again.
Verify if your username is in docker.
If not add again with below commands

```
sudo usermod -aG docker YourUsername
newgrp docker
groups
```
Running initial docker instance
```
sudo systemctl status docker
# Wait for docker to download the hello prg
docker run hello-world     
```

### Bazel

```
sudo apt install apt-transport-https curl gnupg -y
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg

sudo mv bazel-archive-keyring.gpg /usr/share/keyrings

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

sudo apt update && sudo apt install bazel

bazel --version
sudo apt update && sudo apt install bazel-8.1.1

```


### Install liboqs and liboqs-go

Build and install liboqs

```
cd /tmp
# Clean up if exists
rm -rf liboqs  

# Clone repository
git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs.git
cd liboqs

# Configure
mkdir -p build && cd build

cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_SHARED_LIBS=ON ..

# Compile (takes 2-8 minutes)
ninja

# Install
sudo ninja install
sudo ldconfig

```
Verify liboqs
```
# Check installation
ldconfig -p | grep liboqs
pkg-config --modversion liboqs
```
Set up liboqs-go

```
cd /tmp
# Clean up if exists
rm -rf liboqs-go  

# Clone repository
git clone --depth 1 https://github.com/open-quantum-safe/liboqs-go.git
cd liboqs-go
```
Create pkg-config file
```
sudo mkdir -p /usr/local/lib/pkgconfig
```
```
sudo tee /usr/local/lib/pkgconfig/liboqs-go.pc > /dev/null << 'EOF'
prefix=/usr/local
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: liboqs-go
Description: Go bindings for liboqs
Version: 1.0.0
Requires: liboqs
Cflags: -I${includedir}
Libs: -L${libdir} -loqs
EOF
```

verify the last command input
```
nano /usr/local/lib/pkgconfig/liboqs-go.pc 
## exit nano
ctrl+x
```
Update environment
```
# Add to ~/.bashrc
echo '' >> ~/.bashrc
echo '# liboqs and liboqs-go pkg-config path' >> ~/.bashrc
echo 'export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"' >> ~/.bashrc

# Reload
source ~/.bashrc
```
Final verification
```
pkg-config --modversion liboqs
pkg-config --cflags liboqs-go
ldconfig -p | grep liboqs

## output
owner@owner:~$ pkg-config --modversion liboqs
0.15.0
owner@owner:~$ pkg-config --cflags liboqs-go
-I/usr/local/include
owner@owner:~$ ldconfig -p | grep liboqs
	liboqs.so.9 (libc6,x86-64) => /usr/local/lib/liboqs.so.9
	liboqs.so (libc6,x86-64) => /usr/local/lib/liboqs.so
owner@owner:~$ 


```
Clean up

```
cd /tmp
rm -rf liboqs liboqs-go

```



## SCION-SBOM 

If you have existing SCION running, then stop all current SCION and docker containers; else move to Build.
```
./scion.sh stop
docker ps
docker stop $(docker ps -a -q)
```

Verify if your username is in docker group.
If not, add your username in docker group.

```
groups
sudo usermod -aG docker YourUsername
newgrp docker
groups
```


```
cd ~

git clone https://github.com/CNK2100/SCION-SBOM-DEV

cd scion-sbom

./tools/install_bazel

# Install extra dependencies: plumbum-1.6.9 pyyaml-6.0.1 setuptools-69.1.0 six-1.15.0 supervisor-4.2.5 supervisor-wildcards-0.1.3

./tools/install_deps

./scion.sh bazel-remote
```
If you see no container running, wait and try again and you should see below output:
```
 ./scion.sh bazel-remote
WARN[0000] /bazel-remote.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
WARN[0000] No services to build                         
[+] up 1/1
 ✔ Container bazel-remote-cache Running
``` 


Check SCION documentation to build all the package or only SCION services.

https://docs.scion.org/en/latest/dev/build.html

```
## If ERROR: The project you're trying to build requires Bazel 6.4.0 (specified in /home/owner/quantum/.bazelversion), but it wasn't found in /usr/bin. Then install the correct version

sudo apt update && sudo apt install bazel-6.4.0
```
Below "make" command will run for about 3 to 8 minutes depending on your PC specs.
```
make
make test
# Option make test-integration. You may get an error due to the downloading of  "OpenWrt" during test-integration. Just move to the running of SCION
make test-integration
```

## Running SCION Quantum


```
## Locate in scion-sbom folder if not already.
cd ~
cd scion-sbom
make docker-images
## if make docker-images does not run then run first ./scion.sh bazel-remote and then make docker-images
## Run Scion topology
./scion.sh topology -c topology/tiny4.topo 
./scion.sh run
bin/end2end_integration
bin/scion showpaths --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110
```
If you want to see extended details just add --extended

```
bin/scion showpaths --extended --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110

```
Output
```
bin/scion showpaths --extended --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110
Available paths to 1-ff00:0:110
2 Hops:
[0] Hops: [1-ff00:0:112 ~~ 1>2 1-ff00:0:110 ~~]
    MTU: 1400
    NextHop: 127.0.0.25:31012
    PQC-secured: true
    Expires: 2026-01-11 13:45:00 +0000 UTC (5h59m21s)
    SupportsEPIC: false
    Status: alive
    LocalIP: 127.0.0.1
owner@owner:~/quantum$ 
```
### Generate an image of any SCION topology located in /topology/ folder

Generate the topology image
```
./scion.sh topodot -s topology/peering-test.topo
./scion.sh topodot -s topology/peering-test-multi.topo
./scion.sh topodot -s topology/tiny.topo
./scion.sh topodot -s topology/tiny4.topo
./scion.sh topodot -s topology/wide.topo
./scion.sh topodot -s topology/default.topo
./scion.sh topodot -s topology/default-no-peers.topo

```
Stop Scion
```
./scion.sh stop
```

### Troubleshooting

Optional: You may clean the previous installation if you encourter errors
```
make clean
bazel clean
## Not recommanded : remove entire Bazel directory
rm -rf ~/.cache/bazel
```


