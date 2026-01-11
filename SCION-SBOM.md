# Installation of SCION SBOM using QUANTUM

```
## close the terminal and open a new one
groups
cd ~
docker ps
docker stop $(docker ps -a -q)
```

```
mkdir scion-sbom
cd scion-sbom
git clone https://github.com/juagargi/quantum.git
cd quantum
```
Verify if your username is in docker group. If not, add your it.
```
groups
sudo usermod -aG docker YourUsername
newgrp docker
groups
```

Install the scion-sbom
```
./tools/install_bazel
./tools/install_deps
./scion.sh bazel-remote
```
Compile.
Make command will run for about 3 to 8 minutes depending on your PC specs.

```
make
make test
### Optional:  make test-integration
```

### Running SCION Quantum

```
cd scion-sbom/
cd quantum/
make docker-images
./scion.sh topology -c topology/tiny4.topo
./scion.sh run
bin/end2end_integration
bin/scion showpaths --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110

```
If you want to see extended details just add --extended
```
bin/scion showpaths --extended --sciond $(./scion.sh sciond-addr 112) 1-ff00:0:110
```
