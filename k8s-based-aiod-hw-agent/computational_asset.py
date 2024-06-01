import json
from copy import deepcopy

# Metadata model based on the provided JSON schema without "computational_asset" key
metadata_model = {
    "General_properties": {
        "id": "",
        "name": "",
        "geographical_location": "",
        "description": "",
        "owner": "",
        "pricing_schema": "",
        "underlying_orchestrating_technology": "",
        "kernel": "",
        "operating_system": ""
    },
    "HW_Technical_properties": {
        "CPU": {
            "num_cpus": None,
            "num_cpu_cores": None,
            "architecture": None,
            "vendor": None,
            "model_name": None,
            "cpu_family": None,
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
            "num_cores": "",
            "num_gpus": "",
            "architecture": "",
            "vendor": "",
            "model_name": "",
            "type": "",
            "computation_framework_supported": "",
            "memory_size_GB": ""
        },
        "Network": {
            "latency": "",
            "bandwith_Mbps": "",
            "topology": ""
        },
        "Storage": {
            "model": "",
            "vendor": "",
            "capacity_GB": "",
            "type": "",
            "read_bandwith_MBps": "",
            "write_bandwith_MBps": "",
            "data_transfer_mechanisms": ""
        },
        "Memory": {
            "type": "",
            "size_GB": "",
            "bandwith_GBps": "",
            "RDMA": ""
        }
    }
}

class ComputationalAssetManager:
    def __init__(self):
        self.data = deepcopy(metadata_model)
        self.assets = []

    def add_asset(self, asset):
        if not isinstance(asset, dict):
            raise ValueError("Asset should be a dictionary.")
        # Check if the asset matches the structure
        self.assets.append(asset)

    def get_assets(self):
        return self.assets

