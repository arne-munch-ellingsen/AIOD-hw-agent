import redfish
import json
import argparse

# For "old" HPE servers, the standard Storage model from 
# DMTF (https://www.dmtf.org/standards/redfish) is not supported,
# so this will be specific for HPE Gen 10 servers or older
def get_hpe_disk_info(redfish_client):
    all_disk_info = []  # List to hold information of all disk drives
    total_capacity_gb = 0  # Initialize total disk capacity in bytes

    # Get a response from the Redfish service root
    response = redfish_client.get("/redfish/v1")
    systems_uri = response.dict["Systems"]["@odata.id"]
    systems_response = redfish_client.get(systems_uri)
    for system_member in systems_response.dict["Members"]:
        system_uri = system_member["@odata.id"]
        system_response = redfish_client.get(system_uri)

        # Navigate to SmartStorage
        # Assume SmartStorage exists
        smart_storage_uri = system_uri + "/SmartStorage"
        print(f"SmartStorageURI = {smart_storage_uri}")
        smart_storage_response = redfish_client.get(smart_storage_uri)
        # Iterate through ArrayControllers
        if "Links" in smart_storage_response.dict:
            links_uri = smart_storage_response.dict["Links"]["ArrayControllers"]["@odata.id"]
            links_response = redfish_client.get(links_uri)
            for array_controller_member in links_response.dict["Members"]:
                array_controller_uri = array_controller_member["@odata.id"]
                array_controller_response = redfish_client.get(array_controller_uri)

                # Access the DiskDrives for each ArrayController
                if "Links" in array_controller_response.dict:
                    links_drives_uri = array_controller_response.dict["Links"]["PhysicalDrives"]["@odata.id"]
                    links_drives_response = redfish_client.get(links_drives_uri)

                    # Iterate through the DiskDrives collection
                    for disk_drive_member in links_drives_response.dict["Members"]:
                        disk_drive_uri = disk_drive_member["@odata.id"]
                        disk_drive_response = redfish_client.get(disk_drive_uri)

                        # Extract disk drive information and accumulate capacity
                        capacity_gb = disk_drive_response.dict.get("CapacityGB", 0)
                        total_capacity_gb += capacity_gb

                        disk_info = {
                            "Id": disk_drive_response.dict.get("Id", "N/A"),
                            "Name": disk_drive_response.dict.get("Name", "N/A"),
                            "Model": disk_drive_response.dict.get("Model", "N/A"),
                            "CapacityGB": capacity_gb,
                            "BlockSizeBytes": disk_drive_response.dict.get("BlockSizeBytes", "N/A"),
                            "InterfaceSpeedMbps": disk_drive_response.dict.get("InterfaceSpeedMbps", "N/A"),
                            "RotationalSpeedRpm": disk_drive_response.dict.get("RotationalSpeedRpm", "N/A"),
                            "MediaType": disk_drive_response.dict.get("MediaType", "N/A"),
                            "SerialNumber": disk_drive_response.dict.get("SerialNumber", "N/A")
                        }
                        all_disk_info.append(disk_info)

    return {
        "TotalStorageCapacityGB": total_capacity_gb,
        "DiskDrives": all_disk_info
    }
# This is according to DMTF standard
def get_memory_info(redfish_client):
    all_memory_info = []  # List to hold information of all memory modules
    total_capacity_mib = 0  # Initialize total memory capacity in MiB

    # Get a response from the Redfish service root
    response = redfish_client.get("/redfish/v1")

    # Access the Systems collection
    systems_uri = response.dict["Systems"]["@odata.id"]
    systems_response = redfish_client.get(systems_uri)

    # Iterate through the Systems collection
    for system_member in systems_response.dict["Members"]:
        system_uri = system_member["@odata.id"]
        system_response = redfish_client.get(system_uri)

        # Access the Memory collection
        if "Memory" in system_response.dict:
            memory_uri = system_response.dict["Memory"]["@odata.id"]
            memory_response = redfish_client.get(memory_uri)

            # Iterate through the Memory collection
            for memory_member in memory_response.dict["Members"]:
                memory_uri = memory_member["@odata.id"]
                memory_response = redfish_client.get(memory_uri)

                # Extract memory information if CapacityMiB is greater than zero
                capacity_mib = memory_response.dict.get("CapacityMiB", 0)
                if capacity_mib > 0:
                    total_capacity_mib += capacity_mib  # Accumulate the total memory capacity

                    # Navigate to the Oem -> Hpe path to get MaxOperatingSpeedMTs
                    max_speed = memory_response.dict.get("Oem", {}).get("Hpe", {}).get("MaxOperatingSpeedMTs", "N/A")

                    memory_info = {
                        "Id": memory_response.dict.get("Id", "N/A"),
                        "Name": memory_response.dict.get("Name", "N/A"),
                        "MemoryType": memory_response.dict.get("MemoryType", "N/A"),
                        "MemoryDeviceType": memory_response.dict.get("MemoryDeviceType", "N/A"),
                        "CapacityMiB": capacity_mib,
                        "MaxOperatingSpeedMTs": max_speed,
                        "Manufacturer": memory_response.dict.get("Manufacturer", "N/A"),
                        "SerialNumber": memory_response.dict.get("SerialNumber", "N/A")
                    }
                    all_memory_info.append(memory_info)

    # Convert total capacity from MiB to GB (1 GiB = 1024 MiB)
    total_capacity_gb = total_capacity_mib / 1024

    return {
        "TotalMemoryGB": total_capacity_gb,
        "MemoryModules": all_memory_info
    }

# This is according to DMTF standard
def get_cpu_info(redfish_client):
    all_cpus_info = []  # List to hold information of all CPUs
    total_cores = 0  # Initialize total cores
    total_threads = 0  # Initialize total threads

    # Get a response from the Redfish service root
    response = redfish_client.get("/redfish/v1")

    # Access the Systems collection
    systems_uri = response.dict["Systems"]["@odata.id"]
    systems_response = redfish_client.get(systems_uri)

    # Iterate through the Systems collection
    for system_member in systems_response.dict["Members"]:
        system_uri = system_member["@odata.id"]
        system_response = redfish_client.get(system_uri)

        # Access the Processors collection
        if "Processors" in system_response.dict:
            processors_uri = system_response.dict["Processors"]["@odata.id"]
            processors_response = redfish_client.get(processors_uri)

            # Iterate through the Processors collection
            for processor_member in processors_response.dict["Members"]:
                processor_uri = processor_member["@odata.id"]
                processor_response = redfish_client.get(processor_uri)

                # Extract CPU information
                total_cores += processor_response.dict.get("TotalCores", 0)
                total_threads += processor_response.dict.get("TotalThreads", 0)

                cpu_info = {
                    "Model": processor_response.dict.get("Model", "N/A"),
                    "ProcessorArchitecture": processor_response.dict.get("ProcessorArchitecture", "N/A"),
                    "InstructionSet": processor_response.dict.get("InstructionSet", "N/A"),
                    "VendorId": processor_response.dict.get("VendorId", "N/A"),
                    "CoresEnabled": processor_response.dict.get("CoresEnabled", "N/A"),
                    "TotalCores": processor_response.dict.get("TotalCores", "N/A"),
                    "TotalThreads": processor_response.dict.get("TotalThreads", "N/A")
                }
                all_cpus_info.append(cpu_info)

    return {
        "TotalCores": total_cores,
        "TotalThreads": total_threads,
        "CPUs": all_cpus_info
    }

def main(redfish_url, username, password):
    # Create a Redfish client instance
    redfish_client = redfish.redfish_client(base_url=redfish_url, username=username, password=password, \
                                            default_prefix="/redfish/v1/")
    redfish_client.login(auth="session")

    try:
        cpu_info = get_cpu_info(redfish_client)
        memory_info = get_memory_info(redfish_client)
        storage_info = get_hpe_disk_info(redfish_client)

        # Combine CPU and Memory Information
        server_info = {
            "CPUs": cpu_info,
            "Memory": memory_info,
            "Storage": storage_info
        }

        print(json.dumps(server_info, indent=4))

    finally:
        # Logout from the Redfish session
        redfish_client.logout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get CPU and Memory information from a Redfish-enabled server.")
    parser.add_argument("url", help="URL of the Redfish service")
    parser.add_argument("user", help="Username for the Redfish service")
    parser.add_argument("password", help="Password for the Redfish service")

    args = parser.parse_args()
    main(args.url, args.user, args.password)
