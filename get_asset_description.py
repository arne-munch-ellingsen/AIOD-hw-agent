import json
import subprocess

# Function to parse the output of the lscpu command
def parse_lscpu_output(lscpu_output):
    lines = lscpu_output.strip().split("\n")
    cpu_info_dict = {}
    for line in lines:
        split_line = line.split(":")
        key = split_line[0].strip().replace(' ', '_').replace('(', '').replace(')', '').lower()
        value = split_line[1].strip()
        cpu_info_dict[key] = value

    return cpu_info_dict

# Function to parse the output of the nvidia-smi command
def parse_smi_output(smi_output):
    # Split the output into lines for each GPU
    gpu_lines = smi_output.strip().split('\n')

    # Initialize the dictionary to store GPU information
    gpu_info_dict = {'gpus': len(gpu_lines)}

    # Parse each line and add the information to the dictionary
    for index, line in enumerate(gpu_lines, start=1):
        gpu_data = line.split(', ')
        gpu_name = gpu_data[0].strip()
        gpu_memory = gpu_data[1].strip().split(' ')[0]  # Extract memory amount, assume 'MiB' and remove it.

        # Add GPU type and memory info to the dictionary using the index
        gpu_info_dict[f'gpu{index}/type{index}'] = gpu_name
        gpu_info_dict[f'gpu{index}/mem{index}'] = gpu_memory

    return gpu_info_dict

def get_gpu_info():
    # Run the nvidia-smi command and capture the output
    try:
        smi_output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=gpu_name,memory.total,driver_version", "--format=csv,noheader"],
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running nvidia-smi: {e.output}")
        return None

    # Use the parse function to get a dict from the SMI output
    return parse_smi_output(smi_output)

# Function to get CPU information
def get_cpu_info():
    # Replace this with the actual command or method to get CPU info
    # Example: use lscpu command on Unix
    lscpu_info = subprocess.check_output(["lscpu"], text=True)
    cpu_info = parse_lscpu_output(lscpu_info)
    return cpu_info

def get_hostnamectl_info():
    try:
        result = subprocess.run(['hostnamectl', 'status'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running hostnamectl: {e}")
        return None

def parse_hostnamectl_output(output):
    data = {}
    for line in output.splitlines():
        key, value = line.strip().split(': ', 1)
        data[key] = value
    return data


def get_host_info():
    hostnamectl_info = get_hostnamectl_info()
    print(hostnamectl_info)
    host_info = parse_hostnamectl_output(hostnamectl_info)
    return host_info

# Function to compile the server's capability description
def compile_server_description(cpu_info, gpu_info, host_info, file_path, aiod_path):
    # aiod_pre = get_aiod_preamble()
    with open(aiod_path, 'r') as aiod_file:
        aiod_code = aiod_file.read()
    # Read information from the file
    with open(file_path, 'r') as file:
        file_data = json.load(file)
    

    # Create a dictionary structure for the description
    edge_description = {
        #"plantuml_code": plantuml_code,
        #"computational_asset_type": file_data.get("computational_asset_type", 'Unknown'),
        "description": {
            "id": file_data.get("id", 'Unknown'),
            "name": file_data.get("name", 'Unknown'),
            "owner": file_data.get("owner", 'Unknown'),
            "location": file_data.get("location", 'Unknown'),
            "5G_cellular_network_latency_ms": file_data.get("5G_cellular_network_latency_ms", 'Unknown'),
            "operating_system": host_info.get('Operating System', 'Unknown'),
            "kernel": host_info.get('Kernel', 'Unknown'),
            "num_cpu_cores": cpu_info.get('cpus', 'Unknown'),
            "cpus": {
                "architecture": cpu_info.get('architecture', 'Unknown'),
                "model_name": cpu_info.get('model_name', 'Unknown'),
                "cpu_family": cpu_info.get('cpu_family', 'Unknown'),
                "model": cpu_info.get('model', 'Unknown'),
            },
            "num_gpus": gpu_info.get('gpus', 'Unknown'),
            "gpus": {},
        }
    }

    # Iterate over the GPUs and insert type and mem information
    for i in range(1, edge_description["description"]["num_gpus"] + 1):
        gpu_key = f"gpu{i}"
        type_key = f"type{i}"
        mem_key = f"mem{i}"
        edge_description["description"]["gpus"][f"{gpu_key}/{type_key}"] = gpu_info.get(f"{gpu_key}/{type_key}", 'Unknown')
        edge_description["description"]["gpus"][f"{gpu_key}/{mem_key}"] = gpu_info.get(f"{gpu_key}/{mem_key}", 'Unknown')

    # Convert the description to JSON
    return json.dumps(edge_description, indent=4)

# Main function to execute the automation process
def main():
    # Get CPU and GPU information
    cpu_info = get_cpu_info()
    #print(cpu_info)
    gpu_info = get_gpu_info()
    #print(gpu_info)
    host_info = get_host_info()
    #print(host_info)
    # Compile the server description
    description_json = compile_server_description(cpu_info, gpu_info, host_info, "/storageHD/userHome/arneme/edge_description.json", "/storageHD/userHome/arneme/aiod_preamble.json")
    
    # Output the JSON description
    print(description_json)

    # Optionally, you can write this JSON to a file
    with open('server_description.json', 'w') as file:
        file.write(description_json)

# Execute the main function
if __name__ == "__main__":
    main()
