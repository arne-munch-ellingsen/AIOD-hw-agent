import requests
import json

# Define the payload
payload = {
    "platform": "telenor",
    "platform_resource_identifier": "2",
    "name": "edge_tromso_1",
    "description": json.dumps({
        "General_properties": {
            "id": "telenor-1",
            "geographical_location": "",
            "description": "",
            "owner": "Telenor Norway",
            "pricing_schema": "free",
            "underlying_orchestrating_technology": "Kubernetes microk8s",
            "kernel": "5.15.0-101-generic",
            "operating_system": "Ubuntu 22.04.4 LTS"
        },
        "HW_Technical_properties": {
            "CPU": {
                "num_cpus": 40,
                "num_cpu_cores": None,
                "architecture": "amd64",
                "vendor": "Intel",
                "model_name": "Xenon",
                "cpu_family": "6",
                "clock_speed": None,
                "Cache": {
                    "cache_L1": None,
                    "cache_L2": None,
                    "cache_L3": None,
                    "cache_L1_D": None,
                    "cache_L1_I": None
                }
            },
            "Accelerator": {
                "type": "NVIDIA-GeForce-GTX-1080-Ti",
                "computation_framework_supported": "cuda",
                "memory_size_GB": "11"
            },
            "Network": {
                "latency": "10ms",
                "bandwith_Mbps": "1GB/s",
                "topology": "5G UPF local breakout"
            },
            "Storage": {
                "model": "",
                "vendor": "",
                "capacity_GB": "102",
                "type": "",
                "read_bandwith_MBps": "",
                "write_bandwith_MBps": "",
                "data_transfer_mechanisms": ""
            },
            "Memory": {
                "type": "",
                "size_GB": "264",
                "bandwith_GBps": "",
                "RDMA": ""
            }
        }
    })
}

# Define the URL for the POST request
url = 'http://127.0.0.1:5003/computational_asset'

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
