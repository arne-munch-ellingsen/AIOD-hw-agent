## AIoD cloud native HW agent
This folder contains the resulting complete PoC of a cloud-native AIoD HW agent. The cloud native HW agent will be deployed as a Demonset to the underlying Kubernetes cluster. 

### Functionality
The cloud native HW agent will:

- Use existing Node Feature Discovery labels to create aiod specific labels (where applicable)
- Add new NFD aiod specific labels using different techniques
- Collect all the aiod specific labels and create a json formatted hw agent metadata description
- Send the HW agent metadata description to the AIoD platform using a mock-up of the AIoD *computational_assets* API
- Send the cluster credentials to the AIoD platform (allowing the AIoD platform to have full control of the cluster

### Limitations
The PoC has been developed on a single node cluster with NVIDIA GPUs and has not been tested on clusters with multiple nodes or other types of accelerators
