import json

# Function to read JSON data from a file
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to write JSON data to a file
def write_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Function to merge JSON data
def merge_json(json1, json2):
    node = json2['items'][0]
    node_status = node['status']
    node_info = node_status['nodeInfo']
    
    # General properties
    json1['computational_asset']['General_properties']['name'] = node['metadata']['name']
    json1['computational_asset']['General_properties']['geographical_location'] = node_status['addresses'][0]['address']
    json1['computational_asset']['General_properties']['kernel'] = node_info['kernelVersion']
    json1['computational_asset']['General_properties']['operating_system'] = node_info['osImage']
    
    # CPU properties
    json1['computational_asset']['HW_Technical_properties']['CPU']['num_cpus'] = int(node_status['capacity']['cpu'])
    json1['computational_asset']['HW_Technical_properties']['CPU']['architecture'] = node_info['architecture']
    json1['computational_asset']['HW_Technical_properties']['CPU']['vendor'] = node['metadata']['labels']['feature.node.kubernetes.io/cpu-model.vendor_id']
    json1['computational_asset']['HW_Technical_properties']['CPU']['cpu_family'] = node['metadata']['labels']['feature.node.kubernetes.io/cpu-model.family']
    
    # Accelerator properties
    json1['computational_asset']['HW_Technical_properties']['Accelerator']['type'] = node['metadata']['labels']['nvidia.com/gpu.product']
    json1['computational_asset']['HW_Technical_properties']['Accelerator']['memory_size_GB'] = node['metadata']['labels']['nvidia.com/gpu.memory']
    
    # Memory properties
    memory_kib = int(node_status['capacity']['memory'].replace('Ki', ''))
    json1['computational_asset']['HW_Technical_properties']['Memory']['size_GB'] = str(memory_kib // 1024)
    
    # Storage properties
    storage_kib = int(node_status['capacity']['ephemeral-storage'].replace('Ki', ''))
    json1['computational_asset']['HW_Technical_properties']['Storage']['capacity_GB'] = str(storage_kib // 1024)
    
    return json1

# File paths
file_path_1 = 'hw_agent_metadata_model.json'
file_path_2 = 'node_feature_discovery.json'
output_file_path = 'merged_json_file.json'

# Read JSON data from files
json_data_1 = read_json_from_file(file_path_1)
json_data_2 = read_json_from_file(file_path_2)

# Merge JSON data
merged_json = merge_json(json_data_1, json_data_2)

# Write merged JSON data to a file
write_json_to_file(merged_json, output_file_path)

# Print merged JSON data
print(json.dumps(merged_json, indent=2))
