# AI4Europe T5.2 AIoD infrastructure integration (a.k.a. AIoD Hardware agent)
The code here represents AI4Europe Task 5.2´s attempt o create mechanisms that can collect information about an AIoD __*computational_asset*__ and send the info to the AIoD platform using the [AIOD-rest-api](https://github.com/aiondemand/AIOD-rest-api/tree/develop). The **DMTF Redfish**, **User space** and **Kubernetes NFD** examples represents explorations performed to decide how to finally create a cloud native HW agent for AIoD. The [**AIoD cloud native HW agent**](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/k8s-based-aiod-hw-agent) is the final result and is a Proof of Concept implementation of a AIoD HW agent deployed as a DeamonSet to the Kubernetes cluster that is made available to the AIoD platform. We have tested this implementation on a Sun Micro server with 8 NVIDIA GPUs. The same concept could probably be used in Kubernetes clusters on Virtual Machines in a larger Edge datacenters, but this has not been verified.

## DMTF Redfish examples
The [redfish](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/redfish) folder contains early examples for retrieving hardware properties for a server using the DMTF Redfish standardized __*lights out*__ remote access API. The Redfish API can be used in python through the __*redfish*__ package. This way of retrieving the hardware information will work remotely even when the server is turned off (hence the __*lights out*__ name). The Redfish API also contains API calls to control the (bare metal) server and could for example be used to boot an AIoD specific ISO image and manage network settings on the server. Handing the authentication and authorization credentials for Redfish to the AIoD platform will make it possible for the AIoD platform to remotely manage bare metal servers and lend them to users in the same way as Chameleon Cloud is doing it. [Chameleon Cloud](https://www.chameleoncloud.org) handles bare metal servers using Redfish through the OpenStack Ironic functionality. Ironic uses Redfish to handle remote servers.

## User space examples
The [user_space](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/user_space) folder contains the first examples for retrieving hardware properties for a server running code as a user under the servers operating system. This way will only work if the server is up and running, the user logs in and runs the script.

## Kubernetes NFD based example
The [nfd](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/nfd) folder contains explorations towards creating a cloud-native (i.e. Kubernetes based) AIoD HW agent. We have concluded that this is the way to go for making cloud native (e.g. Kubernetes based) 5G Edge computing resources available for the AIoD platform.

## AIoD cloud native HW agent
The [k8s-based-aiod-hw-agent](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/k8s-based-aiod-hw-agent) folder contains the resulting complete PoC of a cloud-native AIoD HW agent. The cloud native HW agent will be deployed as a Demonset to the underlying Kubernetes cluster. 

### Functionality
The cloud native HW agent will:

- Use existing Node Feature Discovery labels to create aiod specific labels (where applicable)
- Add new NFD aiod specific labels using different techniques
- Collect all the aiod specific labels and create a json formatted hw agent metadata description
- Send the HW agent metadata description to the AIoD platform using a mock-up of the AIoD *computational_assets* API
- Send the cluster credentials to the AIoD platform (allowing the AIoD platform to have full control of the cluster

### Limitations
The PoC has been developed on a single node cluster with NVIDIA GPUs and has not been tested on clusters with multiple nodes or other types of accelerators
