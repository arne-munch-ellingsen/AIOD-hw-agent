# Setup microk8s and deploy an application
This is a small example of a kubernetes application that sets a Node Feature Discovery label. It has been tested on odin.

## Install microk8s
```
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
# Add support for the GPUs in the cluster. This will also install the NVIDIA GPU operator
# and thereby also generating the NVIDIA GPU related NFD labels.
microk8s enable gpu
```

## Optionally add support for remote access to the cluster
It is convenient to have remote access to the cluster. Here is how to add that to your local host:
```
# On the microk8s host
microk8s.kubectl config view --raw > config

# Copy the config file to your local .kube/config file. Example using scp:
scp user@host:/path/config ~/.kube
# NB: substitute user@host with username and hostname of the computer where microk8s is installed
#     and path with the path to where the config file was generated with the view command above
```
How to solve this in the real AIoD setting is TBD, but we will transfer the config to the AIoD platform

## Build and deploy application that sets a NFD label to microk8s
Build the docker container and convert it (docker save) to tar format and import it into the microk8s containerd (doing it this way makes use of external docker repo unnecessary).
```
docker build -t k8s-aiod-hw-agent:latest .
docker save k8s-aiod-hw-agent:latest | microk8s ctr image import -
```

Deploy the containerised app:
`microk8s kubectl apply -f deployment.yaml`

## Other useful commands
**List the microk8s images:**
`microk8s ctr images list`

**Remove an image:**
`microk8s ctr images rm <image-name>:<tag>`

**Delete the k8s-aiod-hw-agent image:**
`microk8s ctr images rm docker.io/library/k8s-aiod-hw-agent:latest`

**Get info about the deployed k8s-aiod-hw-agent deamonset**
`microk8s kubectl get pods -l app=k8s-aiod-hw-agent-daemonset`
`microk8s kubectl describe pod <pod-name>`
`microk8s kubectl logs <pod-name>`

**Delete the k8s-aiod-hw-agent deamonset**
kubectl delete daemonset k8s-aiod-hw-agent-daemonset


