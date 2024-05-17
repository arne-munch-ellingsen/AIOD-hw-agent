from kubernetes import client, config

def create_nfd_tag(node_name, tag_key, tag_value):
    # Load kubeconfig or use in-cluster configuration
    config.load_kube_config(config_file='/var/snap/microk8s/current/credentials/client.config')

    # Create an instance of the CoreV1Api
    v1 = client.CoreV1Api()

    # Get the current node object
    node = v1.read_node(name=node_name)

    # Create a new label
    if node.metadata.labels is None:
        node.metadata.labels = {}
    node.metadata.labels[tag_key] = tag_value

    # Update the node with the new label
    v1.patch_node(name=node_name, body=node)

    print(f"NFD tag {tag_key}={tag_value} added to node {node_name}")

node_name = "odin"

# Create some tags with names taken from the HW agent metadata model
tag_key = "ai4europe.aiod/id"
tag_value = "telenor-edge-norway-tromso-1"
create_nfd_tag(node_name, tag_key, tag_value)

tag_key = "ai4europe.aiod/name"
tag_value = "tromso-1"
create_nfd_tag(node_name, tag_key, tag_value)

tag_key = "ai4europe.aiod/geographical-location"
tag_value = "69.65691644431789-18.926948341998617"
create_nfd_tag(node_name, tag_key, tag_value)

