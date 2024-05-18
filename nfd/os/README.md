# Standalone python example programs exploring how to add custom NFD labels
This folder holds example code for the first exploration of how to add custom NFD labels. The programs are just simple python programs that can be executed directly under the operating system on odin.

## Create a "private" python environment
To run the code it is necessary to setup a "private" python environment in order not to mess up settings for other users on odin. Here is how to do that:
```
# Move into the directory where the code is located on odin
cd /home/arneme/microk8s/nfd/os
# Create a private python environment
python3 -m venv nfd
# Activate the private python environment
source nfd/bin/activate
```

## Install needed python modules and run example programs
```
# Install the kubernetes module (allowing the python program to use the kubernetes API to sed NFD labels)
pip install kubernetes
# Run the program that gets the currently set NFD labels
python get_nfd_labels.py
# Run the program that sets three new custom NFD labels (ai4europe.aiod/id, ai4europe.aiod/name, ai4europe.aiod/geographical-location)
python create_nfd_label.py
# Run the program that deletes some labels that I created as a test (not there anymore, but program can be modified to delete the ones crated by the create_nfd_label.py program
python delete_nfd_label
```
