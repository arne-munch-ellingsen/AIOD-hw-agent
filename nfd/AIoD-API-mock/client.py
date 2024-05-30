import requests
import json
import base64
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

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

# Read the text blob from a file
with open("aiod-cluster-config", "r") as text_blob_file:
    text_blob = text_blob_file.read()

# Generate a random AES key
aes_key = os.urandom(32)  # AES-256 key

# Encrypt the text blob using AES
iv = os.urandom(16)  # AES block size is 16 bytes
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()

# Pad the data to be a multiple of the block size
padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
padded_data = padder.update(text_blob.encode()) + padder.finalize()

# Encrypt the padded data
encrypted_blob = encryptor.update(padded_data) + encryptor.finalize()

# Encrypt the AES key with the RSA public key
encrypted_key = public_key.encrypt(
    aes_key,
    asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Encode the encrypted blob and key in base64
encrypted_blob_b64 = base64.urlsafe_b64encode(iv + encrypted_blob).decode()
encrypted_key_b64 = base64.urlsafe_b64encode(encrypted_key).decode()

# Define the URL and headers for the POST requests
comp_asset_url = 'https://127.0.0.1:5003/computational_asset'
credential_url = 'https://127.0.0.1:5003/receive_k8s_credentials'
headers = {'Authorization': 'Bearer your-auth-token'}

# Send the POST request for computational_asset
comp_asset_response = requests.post(comp_asset_url, json=comp_asset_payload, headers=headers, verify='cert.pem')

# Print the computational_asset response
print("Computational Asset Status Code:", comp_asset_response.status_code)
print("Computational Asset Response JSON:", comp_asset_response.json())

# Define the payload for the encrypted text blob
blob_payload = {
    'encrypted_key': encrypted_key_b64,
    'blob': encrypted_blob_b64
}

# Send the POST request for the encrypted text blob
blob_response = requests.post(credential_url, json=blob_payload, headers=headers, verify='cert.pem')

# Print the encrypted text blob response
print("Encrypted Blob Status Code:", blob_response.status_code)
print("Encrypted Blob Response JSON:", blob_response.json())
