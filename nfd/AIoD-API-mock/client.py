import requests
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Load the public key
with open("public_key.pem", "rb") as public_key_file:
    public_key = serialization.load_pem_public_key(public_key_file.read())

# Define the payload for computational_asset API
comp_asset_payload = {
    "platform": "telenor",
    "platform_resource_identifier": "2",
    "name": "edge_tromso_1",
    "description": json.dumps({
        "General_properties": {
            "id": "",
            "name": "telenor_norway_edge_tromso_1",
            "geographical_location": "69.65701421550283, 18.92680415215589",
            "description": "",
            "owner": "Telenor Norway",
            "pricing_schema": "free",
            "underlying_orchestrating_technology": "Kubernetes",
            "kernel": "5.15.0-101-generic",
            "operating_system": "Ubuntu 22.04.4 LTS"
        },
        "HW_Technical_properties": {
            "CPU": {
                "num_cpus": 40,
                "num_cpu_cores": None,
                "architecture": "amd64",
                "vendor": "Intel",
                "model_name": "",
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

# Define the Kubernetes credentials
k8s_credentials = {
    'api_server': 'https://my-k8s-cluster.example.com',
    'user': 'aiod-user',
    'token': 'example-k8s-token'
}

# Encrypt the Kubernetes credentials
credentials_json = json.dumps(k8s_credentials).encode()
encrypted_credentials = public_key.encrypt(
    credentials_json,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
encrypted_credentials_b64 = base64.urlsafe_b64encode(encrypted_credentials).decode()

# Define the URL and headers for the POST requests
comp_asset_url = 'https://127.0.0.1:5003/computational_asset'
k8s_url = 'https://127.0.0.1:5003/receive_k8s_credentials'
headers = {'Authorization': 'Bearer your-auth-token'}

# Send the POST request for computational_asset
comp_asset_response = requests.post(comp_asset_url, json=comp_asset_payload, headers=headers, verify='cert.pem')

# Print the computational_asset response
print("Computational Asset Status Code:", comp_asset_response.status_code)
print("Computational Asset Response JSON:", comp_asset_response.json())

# Define the payload for the Kubernetes credentials
k8s_payload = {'credentials': encrypted_credentials_b64}

# Send the POST request for the Kubernetes credentials
k8s_response = requests.post(k8s_url, json=k8s_payload, headers=headers, verify='cert.pem')

# Print the Kubernetes credentials response
print("Kubernetes Credentials Status Code:", k8s_response.status_code)
print("Kubernetes Credentials Response JSON:", k8s_response.json())
