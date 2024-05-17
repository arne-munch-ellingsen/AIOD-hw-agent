import json

# Load the JSON data from files
with open('hw_agent_metadata_model.json') as f:
    first_json = json.load(f)

with open('node_feature_discovery.json') as f:
    second_json = json.load(f)

# Extract relevant data from the second JSON
second_json_item = second_json['items'][0]

# Merge data into the first JSON
first_json['computational_asset']['General_properties']['name'] = second_json_item['metadata']['name']
first_json['computational_asset']['General_properties']['kernel'] = second_json_item['status']['nodeInfo']['kernelVersion']
first_json['computational_asset']['General_properties']['operating_system'] = second_json_item['status']['nodeInfo']['osImage']
first_json['computational_asset']['General_properties']['geographical_location'] = second_json_item['metadata']['annotations']['projectcalico.org/IPv4Address']

first_json['computational_asset']['HW_Technical_properties']['num_cores'] = second_json_item['status']['capacity']['cpu']
first_json['computational_asset']['HW_Technical_properties']['architecture'] = second_json_item['status']['nodeInfo']['architecture']
first_json['computational_asset']['HW_Technical_properties']['vendor'] = second_json_item['metadata']['labels']['feature.node.kubernetes.io/cpu-model.vendor_id']
first_json['computational_asset']['HW_Technical_properties']['Network']['latency'] = second_json_item['metadata']['annotations'].get('network-latency', '')
first_json['computational_asset']['HW_Technical_properties']['Network']['bandwith_Mbps'] = second_json_item['metadata']['annotations'].get('network-bandwidth', '')

first_json['computational_asset']['HW_Technical_properties']['Accelerator']['type'] = second_json_item['metadata']['labels'].get('nvidia.com/gpu.product', '')
first_json['computational_asset']['HW_Technical_properties']['Accelerator']['memory_size_GB'] = str(int(second_json_item['metadata']['labels'].get('nvidia.com/gpu.memory', '0')) / 1024)

first_json['computational_asset']['HW_Technical_properties']['Memory']['size_GB'] = str(int(second_json_item['status']['capacity']['memory'].replace('Ki', '')) / (1024 ** 2))

# Write the merged data back to the file
with open('merged.json', 'w') as f:
    json.dump(first_json, f, indent=2)

print("Merge completed successfully.")
