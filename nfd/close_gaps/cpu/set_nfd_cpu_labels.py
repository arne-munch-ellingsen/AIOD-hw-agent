import psutil
import re
import subprocess
from kubernetes import client, config
from kubernetes.client.rest import ApiException

LABEL_VALUE_PATTERN = re.compile(r'(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?')

def get_cache_info():
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
    
    return cache_info

def get_cpu_info():
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
    
    return cpu_model_name, cpu_clockspeed

def count_physical_cpus():
    with open('/proc/cpuinfo', 'r') as f:
        physical_ids = set()
        for line in f:
            if line.startswith('physical id'):
                physical_ids.add(line.strip().split()[-1])
    return len(physical_ids)

def sanitize_label_value(value):
    if LABEL_VALUE_PATTERN.fullmatch(value):
        return value
    sanitized_value = re.sub(r'[^A-Za-z0-9_.-]', '_', value)
    sanitized_value = re.sub(r'^[^A-Za-z0-9]+', '', sanitized_value)
    sanitized_value = re.sub(r'[^A-Za-z0-9]+$', '', sanitized_value)
    return sanitized_value if LABEL_VALUE_PATTERN.fullmatch(sanitized_value) else ""

def format_label_value(value):
    sanitized_value = sanitize_label_value(value)
    return sanitized_value if sanitized_value else "unknown"

def load_k8s_config():
    try:
        # Try to load in-cluster configuration
        config.load_incluster_config()
    except config.config_exception.ConfigException:
        # Fallback to kube config file
        config.load_kube_config()

def set_node_labels(node_name, labels):
    v1 = client.CoreV1Api()
    try:
        node = v1.read_node(node_name)
        existing_labels = node.metadata.labels
        if existing_labels is None:
            existing_labels = {}
        existing_labels.update(labels)
        body = {
            "metadata": {
                "labels": existing_labels
            }
        }
        v1.patch_node(node_name, body)
        print(f"Successfully set labels {labels} on node {node_name}")
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->patch_node: {e}")

def set_nfd_labels():
    cpu_model_name, cpu_clockspeed = get_cpu_info()
    cache_info = get_cache_info()
    # Format the clock speed as a label value
    cpu_clockspeed_label = f"{cpu_clockspeed:.0f}MHz" if cpu_clockspeed is not None else "unknown"
    print(f"num_cpus={format_label_value(str(count_physical_cpus()))}")
    print(f"cpu_model_name={format_label_value(cpu_model_name)}")
    print(f"cpu_clockspeed_label={format_label_value(cpu_clockspeed_label)}")
    for cache_name, cache_size in cache_info.items():
        print(f"ai4europe.aiod/{cache_name}={cache_size}")
    # Define the cpu labels
    labels = {
        "ai4europe.aiod/num_cpus": format_label_value(str(count_physical_cpus())),
        "ai4europe.aiod/cpu_model_name": format_label_value(cpu_model_name),
        "ai4europe.aiod/cpu_clockspeed": format_label_value(cpu_clockspeed_label)
    }
    # Add the cache labels
    for cache_name, cache_size in cache_info.items():
        labels[f"ai4europe.aiod/{cache_name}"] = cache_size

    load_k8s_config()
    node_name = open("/etc/hostname").read().strip()
    set_node_labels(node_name, labels)

if __name__ == '__main__':
    set_nfd_labels()
