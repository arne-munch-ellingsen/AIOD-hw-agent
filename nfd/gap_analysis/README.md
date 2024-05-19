# Gap analysis between the HW agent metamodel and the Node Feature Discovery labels
This folder contains information related to the gap analysis.

## The HW agent metadata model
The file [hw_agent_metadata_model.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/hw_agent_metadata_model.json) contains the elements in json format found in the v4 HW agent metadata model mural found [here](https://app.mural.co/t/iti1211/m/iti1211/1700755468143/3ec0180dcadfdb820520d34e8f6b16e3e877252b?sender=5a46dd89-6989-44b8-a18a-b0faa92d622d).

## The default Node Feature Dicovery labels
The file [node_feature_discovery.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/node_feature_discovery.json) contains the default node feature discovery model after the NVIDIA GPU operator has been deployed to the microk8s Kubernetes cluster that we are using for the experimentation.

The comparison between the two files will show the gaps.

As a start, the file [hw_agent_metadatamodel_with_values_from_node_labels.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/hw_agent_metadatamodel_with_values_from_node_labels.json) is a representation of the HW agent metadata with values taken from NFD labels. Empty values identifies the gaps.

## Gap summary
In the **General_properties** part of the HW agen model, only the "kernel" and the "operating_system" part can be deduced from the NFD labels. These fields are missing:
* "id"  # Is this an id assigned by the AIoD platform or by the provider of the HW?
* "name" # hostname of node?
* "geographical_location" # Lat, long format?
* "description"
* "owner"
* "pricing_schema"
* "underlying_orchestrating_technology"

In the **"HW_Technical_properties" "CPU"** section, most info can be filled in, except for the *cache* part and *cpu clock_speed*, *num_cpus* and *model name*.

In the **"HW_Technical_properties" Accelerator** section all parts can be filled in (assuming that *computation_framework_supported* can be deduced to be *cuda*. ${\color{red}NB:}$ **Note that the HW agent metadata model is itself missing a num_gpus key**.

In the **"HW_Technical_properties" "Network"** section everything is missing. Not sure if the network section is about intra GPU networks or something else? Is it related to Infiniband/RDMA?

In the **"HW_Technical_properties" "Storage" and "Memory"** section everything except the sizes are missing. Not sure if the Memory section is about CPU or GPU memory? Most likely GPU since RDMA is mentioned?
