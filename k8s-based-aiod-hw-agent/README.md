# AIoD cloud native HW agent
The AIoD cloud native HW agent is a complete PoC of a cloud-native (Kubernetes) AIoD HW agent. The cloud native HW agent will be deployed as a Demonset to the underlying Kubernetes cluster. The cloud native HW agent has been tested on a Sun Micro server with 8 NVIDIA GPUs.

## Functionality
The cloud native HW agent will:

- Use existing Node Feature Discovery labels to create aiod specific labels (where applicable)
- Add new NFD aiod specific labels using different techniques
- Collect all the aiod specific labels and create a json formatted hw agent metadata description
- Send the HW agent metadata description to the AIoD platform using a mock-up of the AIoD *computational_assets* API
- Send the cluster credentials to the AIoD platform (allowing the AIoD platform to have full control of the cluster

## Prerequsites
The HW agent will use the AIoD *computational_asset* API to send a description of the resources available. This API is currently not conformant with the HW agent metadata model and can only receive a maximum of 1800 bytes of JSON formatted descriptions. It is therefore necessary to start the mock-up AIoD API to be able to run the cloud native HW agent succesfully. The AIoD mock-up API can be found [here](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/nfd/AIoD-API-mock). The development of the mock-up API was part of Task 5.2 exploratory work.

**Note** also that we included a few "mandatory" fields from the original AIoD *conmputational_asset* API to the AIoD mock-up API and also added a num_gpus field to the HW agent metadata model.

## Limitations
The PoC has been developed on a single node cluster with NVIDIA GPUs and has not been tested on clusters with multiple nodes or other types of accelerators

## Setup microk8s and deploy an application
This is a small example of a kubernetes application that sets a Node Feature Discovery label. It has been tested on odin.

### Install microk8s
```
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
# Add support for the GPUs in the cluster. This will also install the NVIDIA GPU operator
# and thereby also generating the NVIDIA GPU related NFD labels.
microk8s enable gpu
```

### Optionally add support for remote access to the cluster
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

### Build and deploy the application that sets AIoD related NFD labels and sends a HW agent metadata description to the AIoD platform
Build the docker container and convert it (docker save) to tar format and import it into the microk8s containerd (doing it this way makes use of external docker repo unnecessary).
```
docker build -t k8s-aiod-hw-agent:latest .
docker save k8s-aiod-hw-agent:latest | microk8s ctr image import -
```

Deploy the containerised app:
`microk8s kubectl apply -f deployment.yaml`

### Other useful commands
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


