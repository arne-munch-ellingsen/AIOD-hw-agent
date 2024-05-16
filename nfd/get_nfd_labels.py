from kubernetes import client, config
import json

def get_nfd_labels(node_name):
    # Load the MicroK8s kubeconfig
    config.load_kube_config(config_file='/var/snap/microk8s/current/credentials/client.config')

    # Create an instance of the CoreV1Api
    v1 = client.CoreV1Api()

    # Get the node object
    node = v1.read_node(name=node_name)

    # Filter out NFD labels
    nfd_labels = {key: value for key, value in node.metadata.labels.items() }

    # Print NFD labels in JSON format
    print(json.dumps(nfd_labels, indent=2))

get_nfd_labels("odin")
