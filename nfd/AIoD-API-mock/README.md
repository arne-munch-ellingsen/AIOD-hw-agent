# Mock-up for the AIoD API
We have created a mock-up of the AIoD *computational_asset* API that we can use to create a end-to-end PoC of the cloud native (i.e. Kubernetes) AIoD HW agent. The mock-up API has been created using Flask. We looked at the existing real [AIoD API](https://github.com/aiondemand/AIOD-rest-api) and added the platform and name parameters used for all the other types of assets. It is of course possible to add more fields from the original API if needed (e.g. type, etc.). The HW agent metadata model is included in the "description" field in the POST json payload. This field was introduced by us and could have been called hw-agent-metadata or something similar (TBD).

The HW agent will use this API to send the HW metadata and the Kubernetes cluster credentials to the AIoD platform. The Kubernetes credentials consist of the URL, the username and an admin access token. 

**How the AIoD platform schedules access for AIoD platform users to the cluster is up to the AIoD platform to decide. The credential gives the AIoD platform admin rights of the cluster and the AIoD platform can use the full Kubernetes API to interact with the cluster.**

## Prerequsite
Create the needed keys and certificates for secure communication with the AIoD platform mock-up API:
```
# Create the private and public key
python ./create_keys.py

# Create a self signed certificate (on command line)
openssl req -x509 -new -nodes -key private_key.pem -sha256 -days 365 -out cert.pem -config openssl.cnf

# On the Kubernetes host create microk8s user and token by running the creation script:
./create_credentials.sh

# NB: Copy the displayed token into the client.py program (substitute the example-k8s-token with the token)
```

## Create the docker image
```docker-compose build```

## Usage
To start the Flask App that simulates the AIoD API:

```docker-compose up```

To stop a running instance:

```docker compose down```

To test it run the Python client:

```python client.py```

The mock-up AIoD platform should now have received HW agent metadata and the credentials for the Kubernetes cluster that was made available to the AIoD platform.

