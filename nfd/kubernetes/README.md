# Setup microk8s and deploy an application
This is a small example of a kubernetes application that sets a Node Feature Discovery label. It has been tested on odin.

## Install microk8s
```
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
```
## Build and deploy application that sets a NFD label to microk8s
Build the docker container and convert it (docker save) to tar format and import it into the microk8s containerd (doing it this way makes use of external docker repo unnecessary).
```
docker build -t nfd-labeler:latest .
docker save nfd-labeler:latest | microk8s ctr image import -
```

Deploy the containerised app:
`microk8s kubectl apply -f deployment.yaml`

## Other useful commands
**List the microk8s images:**
`microk8s ctr images list`

**Remove an image:**
`microk8s ctr images rm <image-name>:<tag>`

**Delete the nfd-labler images:**
`microk8s ctr images rm docker.io/library/nfd-labeler:latest`

**Get info about the deployed application**
`microk8s kubectl describe deployment nfd-labler`
`microk8s kubectl get pods`
`microk8s kubectl describe pod <pod-name>`
`microk8s kubectl logs <pod-name>`




