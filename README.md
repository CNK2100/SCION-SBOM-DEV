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
### Installation of Docker
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

```
Install SCION 
```
git clone https://github.com/scionproto/scion
cd scion
./tools/install_bazel
./tools/install_deps
groups  ### Verify again if your username is included in Docker group
./scion.sh bazel-remote ## wait for image to build
make
```
If you get this error: The project you're trying to build requires Bazel 8.1.1
Then install the correct Bazel version
```
sudo apt update && sudo apt install bazel-8.1.1
make   ### Initial make command will take up 5 to 10 minutes depending of your cpu & RAM specs.
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

### Stop SCION
```
./scion.sh stop
```



## SCION QUANTUM INSTALLATION
### Requirements
Install all above SCION depencies if not installed and proceed.

```

```



