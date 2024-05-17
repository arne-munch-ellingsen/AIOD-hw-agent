from kubernetes import client, config
from kubernetes.client.rest import ApiException

def load_k8s_config():
    try:
        # Try to load in-cluster configuration
        config.load_incluster_config()
    except config.config_exception.ConfigException:
        # Fallback to kube config file
        config.load_kube_config()

def set_node_labels(node_name, labels):
    v1 = client.CoreV1Api()
    body = {
        "metadata": {
            "labels": labels
        }
    }
    try:
        v1.patch_node(node_name, body)
        print(f"Successfully set labels {labels} on node {node_name}")
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->patch_node: {e}")

def main():
    load_k8s_config()
    node_name = "odin"
    labels = {
        "ai4europe.aiod/test": "Hello"
    }
    set_node_labels(node_name, labels)

if __name__ == "__main__":
    main()
