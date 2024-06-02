from kubernetes import client, config
from kubernetes.client.rest import ApiException
from computational_asset import metadata_model, ComputationalAssetManager
from send_asset_and_config import DataEncryptorSender
from copy import deepcopy
import json
import psutil
import re
import subprocess
import psutil

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

def get_nfd_labels(asset):
    # Retrieve nodes
    v1 = client.CoreV1Api()
    nodes = v1.list_node()

    for node in nodes.items:
        # Create a new asset based on the metadata model        
        # Set general properties if they do not exist already
        if not asset['General_properties']['name']:
            asset['General_properties']['name'] = node.metadata.name
        if not asset['General_properties']['kernel']:
            asset['General_properties']['kernel'] = node.status.node_info.kernel_version
        if not asset['General_properties']['operating_system']:
            asset['General_properties']['operating_system'] = node.status.node_info.os_image

        # Set HW technical properties if they do not exist
        if not asset['HW_Technical_properties']['CPU']['num_cpus']:
            asset['HW_Technical_properties']['CPU']['num_cpus'] = node.status.capacity.get("cpu")
        if not asset['HW_Technical_properties']['CPU']['architecture']:
            asset['HW_Technical_properties']['CPU']['architecture'] = node.status.node_info.architecture
        if not asset['HW_Technical_properties']['CPU']['vendor']:
            asset['HW_Technical_properties']['CPU']['vendor'] = node.metadata.labels.get("feature.node.kubernetes.io/cpu-model.vendor_id", "")
        if not asset['HW_Technical_properties']['CPU']['cpu_family']:
            asset['HW_Technical_properties']['CPU']['cpu_family'] = node.metadata.labels.get("feature.node.kubernetes.io/cpu-model.family", "")
        if not asset['HW_Technical_properties']['Accelerator']['model_name']:
            asset['HW_Technical_properties']['Accelerator']['model_name'] = node.metadata.labels.get("nvidia.com/gpu.product")
        if not asset['HW_Technical_properties']['Accelerator']['num_gpus']:
            asset['HW_Technical_properties']['Accelerator']['num_gpus'] = node.metadata.labels.get("nvidia.com/gpu.count")
        if not asset['HW_Technical_properties']['Accelerator']['memory_size_GB']:
            asset['HW_Technical_properties']['Accelerator']['memory_size_GB'] = str(int(node.metadata.labels.get("nvidia.com/gpu.memory"))/1024)

def get_cache_info(asset):
    cache_info = {}
    try:
        # Get the full output from lscpu
        lscpu_output = subprocess.check_output("lscpu", shell=True).decode()
        
        # Regex patterns for matching cache sizes
        patterns = {
            "cache_L1_D": r"L1d cache:\s+(\d+\s*[KMG]B?)",
            "cache_L1_I": r"L1i cache:\s+(\d+\s*[KMG]B?)",
            "cache_L2": r"L2 cache:\s+(\d+\s*[KMG]B?)",
            "cache_L3": r"L3 cache:\s+(\d+\s*[KMG]B?)"
        }
        
        # Extract cache sizes using regex patterns
        for cache_name, pattern in patterns.items():
            match = re.search(pattern, lscpu_output)
            if match:
                cache_info[cache_name] = match.group(1).replace(" ", "")
        
        # Combine L1 Data and Instruction cache sizes for total L1 cache size
        if "cache_L1_D" in cache_info and "cache_L1_I" in cache_info:
            l1_d_size = int(cache_info["cache_L1_D"][:-1])  # remove unit and convert to int
            l1_i_size = int(cache_info["cache_L1_I"][:-1])  # remove unit and convert to int
            cache_info["cache_L1"] = f"{l1_d_size + l1_i_size}K"
    except Exception as e:
        print(f"Error retrieving cache information: {e}")
    
    # cache_L1_D
    for cache_name, cache_size in cache_info.items():
        if not asset['HW_Technical_properties']['CPU']['Cache'][cache_name]:
            asset['HW_Technical_properties']['CPU']['Cache'][cache_name] = cache_size


def get_cpu_info(asset):
    cpu_model_name = None
    cpu_clockspeed = None
    
    for cpu_info in psutil.cpu_freq(percpu=True):
        if cpu_clockspeed is None:
            cpu_clockspeed = cpu_info.current  # in MHz
    
    with open('/proc/cpuinfo') as f:
        for line in f:
            if 'model name' in line:
                cpu_model_name = line.split(': ')[1].strip()
                break
    cpu_clockspeed_label = f"{cpu_clockspeed:.0f}MHz" if cpu_clockspeed is not None else "unknown"
    if not asset['HW_Technical_properties']['CPU']['model_name']:
        asset['HW_Technical_properties']['CPU']['model_name'] = convert_cpu_model(cpu_model_name)
    # Could be that this is current clock speed...
    if not asset['HW_Technical_properties']['CPU']['clock_speed']:
        asset['HW_Technical_properties']['CPU']['clock_speed'] = cpu_clockspeed_label

def convert_to_labels(asset):
    labels = {}

    def process_dict(d, parent_key='aiod'):
        for k, v in d.items():
            new_key = f"{parent_key}.{k}".lower().replace(' ', '-')
            if isinstance(v, dict):
                process_dict(v, new_key)
            elif v:  # Only add non-empty values
                new_value = str(v).lower().replace(' ', '-')
                labels[new_key] = new_value

    process_dict(asset)
    return labels

def convert_cpu_model(cpu_model: str) -> str:
    # Remove unwanted characters and extra spaces to make it conformant with a NFD label
    cpu_model = re.sub(r'\(R\)', '', cpu_model)  # Remove (R)
    cpu_model = re.sub(r'CPU', '', cpu_model)  # Remove CPU
    cpu_model = re.sub(r'Intel', '', cpu_model)  # Remove CPU
    cpu_model = re.sub(r'@ \d+\.\d+GHz', '', cpu_model)  # Remove frequency
    cpu_model = re.sub(r'\s+', ' ', cpu_model)  # Replace multiple spaces with single space
    cpu_model = cpu_model.strip()  # Strip leading and trailing spaces

    # Replace spaces with underscores
    cpu_model = cpu_model.replace(' ', '_')
    return cpu_model

def main():
    load_k8s_config()
    node_name = "odin"
    asset_manager = ComputationalAssetManager()
    new_asset = deepcopy(metadata_model)
    # Add the asset template
    asset_manager.add_asset(new_asset)
    # Add asset values that can be retrieved from the already existing node and NFD labels
    get_nfd_labels(new_asset)    
    # Add the cache_info
    get_cache_info(new_asset)
    # Add info about CPU
    get_cpu_info(new_asset)
    
    labels = convert_to_labels(new_asset)
    print(f"Got these labels: {json.dumps(labels, indent=4)}", flush=True)
    # set the created labels as cluster NFD labels
    print("Setting labels:", flush=True)
    # If the cluster changes, these labels will change automatically (this is a property of DeamonSet)
    set_node_labels(node_name, labels)
    # Send the data and cluster config to AIoD
    print("Encrypt and send asset info to AIoD platform:", flush=True)

    encryptor_sender = DataEncryptorSender(
        public_key_path="public_key.pem",
        config_path="aiod-cluster-config", # This is the microk8s config credentials file
        comp_asset_url='https://129.242.22.51:5003/computational_asset',
        credential_url='https://129.242.22.51:5003/k8s_credentials',
        cert_path='cert.pem'
    )
    # Add the "mandatory" fields (platform, platform_resource_identifier and name)
    computational_asset_payload = {
        "platform": "telenor",
        "platform_resource_identifier": "2",
        "name": "edge_tromso_1",
        "description": json.dumps(new_asset)
    }
    
    encryptor_sender.process_and_send(computational_asset_payload)

if __name__ == "__main__":
    main()

