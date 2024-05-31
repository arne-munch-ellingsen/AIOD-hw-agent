# AI4Europe T5.2 AIoD infrastructure integration (a.k.a. AIoD Hardware agent)
The code here represents AI4Europe Task 5.2´s attempt o create mechanisms that can collect information about an AIoD __*computational_asset*__ and send the info to the AIoD platform using the [AIOD-rest-api](https://github.com/aiondemand/AIOD-rest-api/tree/develop).

## Kubernetes NFD based example
The [nfd](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/nfd) folder contains explorations towards creating a cloud-native (i.e. Kubernetes based) AIoD HW agent. We have concluded that this is the way to go for making cloud native (e.g. Kubernetes based) 5G Edge computing resources available for the AIoD platform.

## DMTF Redfish examples
The [redfish[(https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/redfish) folder contains early examples for retrieving hardware properties for a server using the DMTF Redfish standardized __*lights out*__ remote access API. The Redfish API can be used in python through the __*redfish*__ package. This way of retrieving the hardware information will work remotely even when the server is turned off (hence the __*lights out*__ name). The Redfish API also contains API calls to control the (bare metal) server and could for example be used to boot an AIoD specific ISO image and manage network settings on the server. Handing the authentication and authorization credentials for Redfish to the AIoD platform will make it possible for the AIoD platform to remotely manage bare metal servers and lend them to users in the same way as Chameleon Cloud is doing it. [Chameleon Cloud](https://www.chameleoncloud.org) handles bare metal servers using Redfish through the OpenStack Ironic functionality. Ironic uses Redfish to handle remote servers.

## User space examples
The [user_space](https://github.com/arne-munch-ellingsen/AIOD-hw-agent/tree/main/user_space) folder contains the first examples for retrieving hardware properties for a server running code as a user under the servers operating system. This way will only work if the server is up and running, the user logs in and runs the script.
