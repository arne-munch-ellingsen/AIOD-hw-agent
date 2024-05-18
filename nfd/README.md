# Node Feature Discovery example programs
This folder holds example programs from exploration of the Node Feature Discovery (NFD) mechanism in Kubernetes. The intention is to use NFD as a mechanism to obtain the information needed to fill in a complete HW agent metadata model for a Kubernetes cluster with GPU node(s) that wil be made available for users of the AIoD platform developed as part of the AI4Europe project.

## os folder
The os folder contains example programs that runs directly under the operating system of a single node Kubernetes cluster.

## kubernetes folder
THe kubernetes folder contains example programs that runs in the kubernetes cluster.

## gap_analysis folder
This folder cotains stuff related to identifying the gap between what the default Node Feature Discovery labels can´t populate in the HW agent metadata model.

## close_gaps folder
This folder contains example kubernetes containerized apps that retrieves missing values and sets the corresponding aiod NFD label. It will contain supfolders reflecting the section of the HW agent metadata model the example apps relates to.
