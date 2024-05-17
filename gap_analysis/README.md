# Gap analysis between the HW agent metamodel and the Node Feature Discovery lables
This folder contains information related to the gap analysis.

## The HW agent metadata model
The file [hw_agent_metadata_model.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/hw_agent_metadata_model.json) contains the elements in json format found in the v4 HW agent metadata model mural found [here](https://app.mural.co/t/iti1211/m/iti1211/1700755468143/3ec0180dcadfdb820520d34e8f6b16e3e877252b?sender=5a46dd89-6989-44b8-a18a-b0faa92d622d).

The file [node_feature_discovery.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/node_feature_discovery.json) contains the default node feature discovery model after the NVIDIA GPU operator has been deployed to the microk8s Kubernetes cluster that we are using for the experimentation.

The comparison between the two files will show the gaps.

As a start, the file [hw_agent_metadatamodel_with_values_from_node_labels.json](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/blob/main/gap_analysis/hw_agent_metadatamodel_with_values_from_node_labels.json) is a representation of the HW agent metadata with values taken from NFD labels. Emty values identifies the gaps.