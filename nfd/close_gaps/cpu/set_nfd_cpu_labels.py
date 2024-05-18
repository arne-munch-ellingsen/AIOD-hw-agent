import psutil
import re
from kubernetes import client, config
from kubernetes.client.rest import ApiException

LABEL_VALUE_PATTERN = re.compile(r'(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?')

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

def set_nfd_labels():
    cpu_model_name, cpu_clockspeed = get_cpu_info()

    # Format the clock speed as a label value
    cpu_clockspeed_label = f"{cpu_clockspeed:.0f}MHz" if cpu_clockspeed is not None else "unknown"
    print(f"num_cpus={format_label_value(str(count_physical_cpus()))}")
    print(f"cpu_model_name={format_label_value(cpu_model_name)}")
    print(f"cpu_clockspeed_label={format_label_value(cpu_clockspeed_label)}")
    
    # Define the labels
    labels = {
        "ai4europe.aiod/num_cpus": format_label_value(str(count_physical_cpus())),
        "ai4europe.aiod/cpu_model_name": format_label_value(cpu_model_name),
        "ai4europe.aiod/cpu_clockspeed": format_label_value(cpu_clockspeed_label)
    }

    load_k8s_config()
    node_name = open("/etc/hostname").read().strip()
    set_node_labels(node_name, labels)

if __name__ == '__main__':
    set_nfd_labels()
