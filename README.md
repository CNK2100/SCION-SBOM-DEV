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
pip install pyyaml toml plumbum graphviz
sudo apt-get install -y graphviz python3-graphviz
sudo apt-get install -y build-essential cmake git pkg-config libssl-dev ninja-build
sudo apt-get install -y supervisor

```
### Installation of Docker
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/owner@owner:~/quantum$ ./scion.sh bazel-remote
WARN[0000] /home/owner/quantum/bazel-remote.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
WARN[0000] No services to build                         
[+] up 1/1
 ✔ Container bazel-remote-cache Running   ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

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
##verify if your username is in docker or restart your computer to take effect.
If not add again below commands

```
sudo usermod -aG docker YourUsername
newgrp docker
groups
```
Running initial docker instance
```
sudo systemctl status docker
##wait for docker to download the hello prg
docker run hello-world     
```

### Installation of Bazel

```
sudo apt install apt-transport-https curl gnupg -y
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg

sudo mv bazel-archive-keyring.gpg /usr/share/keyrings

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

sudo apt update && sudo apt install bazel

bazel --version

```

### SCION installation

Stop all docker containers: 
```
docker ps
docker stop $(docker ps -a -q)
  sudo apt update && sudo apt install bazel-6.4.0

```
Install SCION 
```
git clone https://github.com/scionproto/scion
cd scion
./tools/install_bazel
./tools/install_deps
### Verify again if your username is included in Docker group
groups  
./scion.sh bazel-remote
## wait for image to build
make
```
If you get this error: The project you're trying to build requires Bazel 8.1.1
Then install the correct Bazel version
```
sudo apt update && sudo apt install bazel-8.1.1
### Initial make command will take up 5 to 10 minutes depending of your cpu & RAM specs.
make   
```

### SCION instalation verification
Verify Scion installation (Optional: You can go directly to Running Scion section.)
During the make test, if you get an error run again make test
You will get the final error:
//private/underlay/ebpf:portfilter_test  FAILED
Executed 2 out of 135 tests: 134 tests pass and 1 fails locally.


```
make test
make test-integration
```
Errors. Just continue to Running SCION

Error with make test
```
//tools/pktgen/cmd/pktgen:go_default_test                       (cached) PASSED in 0.1s
//private/underlay/ebpf:portfilter_test                                  FAILED in 0.0s
  bazel-testlogs/private/underlay/ebpf/portfilter_test/test.log

Executed 1 out of 135 tests: 134 tests pass and 1 fails locally.
There were tests whose specified size is too big. Use the --test_verbose_timeout_warnings command line option to see which ones these are.
make: *** [Makefile:60: test] Error 3

```
Try install
```
sudo apt-get install -y linux-headers-$(uname -r) clang llvm libbpf-dev libelf-dev

```
make test-integration result : Executed 3 out of 24 tests: 21 tests pass and 3 fail locally.
 

```
//tools/cryptoplayground:trc_ceremony_test                      (cached) PASSED in 7.1s
//acceptance/router_benchmark:test                                       FAILED in 1.9s
  bazel-testlogs/acceptance/router_benchmark/test/test.log
//acceptance/router_multi:test_bfd                                       FAILED in 1.0s
  bazel-testlogs/acceptance/router_multi/test_bfd/test.log
//acceptance/router_multi:test_nobfd                                     FAILED in 1.1s
  bazel-testlogs/acceptance/router_multi/test_nobfd/test.log

Executed 3 out of 24 tests: 21 tests pass and 3 fail locally.
There were tests whose specified size is too big. Use the --test_verbose_timeout_warnings command line option to see which ones these are.
make: *** [Makefile:63: test-integration] Error 3

```

### Running SCION
```
cd ~/scion
make docker-images 
./scion.sh topology -c topology/tiny4.topo 
./scion.sh run
bin/end2end_integration  
bin/scion showpaths --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110

```
Show path Extended
```
bin/scion showpaths --extended --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110

```

### Generate an image of any SCION topology located in /topology/ folder
Install requirements
```
pip install pyyaml toml plumbum graphviz
sudo apt-get install -y graphviz python3-graphviz
```
Generate the topology image
```
./scion.sh topodot -s topology/tiny.topo
./scion.sh topodot -s topology/tiny4.topo
./scion.sh topodot -s topology/wide.topo
./scion.sh topodot -s topology/default.topo
./scion.sh topodot -s topology/default-no-peers.topo



```
If you get the error, the issue could be Bazel Python path, not pip.
Then Run this instead:

```
python3 tools/topodot.py -s topology/tiny4.topo
python3 tools/topodot.py -s topology/wide.topo
python3 tools/topodot.py -s topology/tiny.topo
python3 tools/topodot.py -s topology/default-no-peers.topo
python3 tools/topodot.py -s topology/default.topo
```

### Stop SCION
```
./scion.sh stop
```



## SCION QUANTUM INSTALLATION
### Requirements
Install all above SCION depencies if not installed and proceed.
```
sudo apt update
sudo apt upgrade

sudo apt install wget
sudo apt-get install -y graphviz
sudo apt install golang-go
go version
sudo apt install default-jdk
sudo apt install locate
updatedb
pip install pyyaml toml plumbum graphviz
sudo apt-get install -y graphviz python3-graphviz

## SCION Quantum requirement
sudo apt-get install -y build-essential cmake git pkg-config libssl-dev ninja-build
sudo apt-get install -y supervisor

```
Install Docker (see above installation details)
Install Bazel (see above installation details)

Stop all current SCION and docker containers: 
```
./scion.sh stop
docker ps
docker stop $(docker ps -a -q)
```

### Install liboqs and liboqs-go used on SCION quantum

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

# Create pkg-config file
sudo mkdir -p /usr/local/lib/pkgconfig
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

## verify the last command input
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

### Installing SCION QUANTUM
Stop SCION and all docker containers: 
```
./scion.sh stop
docker ps
docker stop $(docker ps -a -q)
```
Verify if your username is in docker group.
If not, add your usernam in docker group.

```
groups
sudo usermod -aG docker YourUsername
newgrp docker
groups
```
Optional: You may clean the previous installation if you encourter errors
```
make clean
bazel clean
## Not recommanded : remove entire Bazel directory
rm -rf ~/.cache/bazel
```

```
cd ~

git clone https://github.com/juagargi/quantum.git

cd quantum

./tools/install_bazel

### Install SCION Quantum extra dependencies: plumbum-1.6.9 pyyaml-6.0.1 setuptools-69.1.0 six-1.15.0 supervisor-4.2.5 supervisor-wildcards-0.1.3

./tools/install_deps

./scion.sh bazel-remote
```
If you see no container running, try again all  above command and you should see below output:
```
owner@owner:~/quantum$ ./scion.sh bazel-remote
WARN[0000] /home/owner/quantum/bazel-remote.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
WARN[0000] No services to build                         
[+] up 1/1
 ✔ Container bazel-remote-cache Running
``` 


Check SCION documentation to build all the package or only SCION services.

https://docs.scion.org/en/latest/dev/build.html

```
## If ERROR: The project you're trying to build requires Bazel 6.4.0 (specified in /home/owner/quantum/.bazelversion), but it wasn't found in /usr/bin.

sudo apt update && sudo apt install bazel-6.4.0

## Make command will run for about 3 to 8 minutes depending on your PC specs.

make
```
Development workflow:
```
make - build after code changes
make test - quick validation
make test-integration - comprehensive testing before commits (optional)

The integration tests simulate real SCION network scenarios,
which is why they take much longer and require more setup (like the OpenWrt that may cause error).
```


```
## Make test command will run for about 3 to 8 minutes depending on your PC specs.
## It will execute 135 out of 135 tests: 135 tests pass.

make test
```
Make test-integration (optional)
```
## Make test-integration command will run for about 3 to 8 minutes depending on your PC specs.
## It may fail to download the openwrt package depending on your network firewal config and speed.
## Then just move to next step.

make test-integration

## Execution #1: Executed 1 out of 17 tests: 1 test passes, 1 fails to build and 15 were skipped.
## Run again  make test-integration
## issue with OpenWrt that needs to be download. You can add it manually in Bazel cache and run again the test
##


```

## Running SCION Quantum

Continue with the installation and run below. If you exit the terminal or restart your installation then run the installation command for creating a docker container:
```
cd ~
cd quantum
./tools/install_bazel
./tools/install_deps
./scion.sh bazel-remote
make
```
Then proceed with running SCION Quantum

```
## Locate in quantum folder if not already.
cd ~
cd quantum
make docker-images
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
Install requirements
```
pip install pyyaml toml plumbum graphviz
sudo apt-get install -y graphviz python3-graphviz
```
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




