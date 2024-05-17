from kubernetes import client, config

def delete_node_label(node_name, label_key):
    # Load the MicroK8s kubeconfig
    config.load_kube_config(config_file='/var/snap/microk8s/current/credentials/client.config')

    # Create an instance of the CoreV1Api
    v1 = client.CoreV1Api()

    # Get the node object
    node = v1.read_node(name=node_name)

    # Check if the label exists
    if node.metadata.labels and label_key in node.metadata.labels:
        # Remove the label using JSON patch
        body = {
            "op": "remove",
            "path": f"/metadata/labels/{label_key.replace('/', '~1')}"
        }

        v1.patch_node(name=node_name, body=[body])

        print(f"Label {label_key} deleted from node {node_name}")
    else:
        print(f"Label {label_key} not found on node {node_name}")

node_name = "odin"

# Some example aiod keys that I did create and deleted using this code
label_key = "ai4europe.aiod/geographical-location-lat"
delete_node_label(node_name, label_key)

label_key = "ai4europe.aiod/geografical-location-long"
delete_node_label(node_name, label_key)
