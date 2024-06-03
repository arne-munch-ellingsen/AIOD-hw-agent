# Setup microk8s and deploy an application
The cloud native HW agent runs in a Kubernetes cluster. We have used the microk8s kubernetes implementation for our PoC. This file describes howto setup microk8s for this usage on a Linux server.

## Install microk8s
```
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s

# Check status
microk8s status --wait-ready
```
When all services are up and running your microk8s cluster is ready.



