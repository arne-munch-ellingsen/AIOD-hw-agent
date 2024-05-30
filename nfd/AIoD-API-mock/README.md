# Mock-up for the AIoD API
We have created a mock-up of the AIoD *computational_asset* API that we can use to create a end-to-end PoC of the cloud native (i.e. Kubernetes) AIoD HW agent. The API has been created using Flask. We looked at the existing real [AIoD API](https://github.com/aiondemand/AIOD-rest-api) and added the platform and name parameters used for all the other types of assets. It is of course possible to add more fields from the original API if needed (e.g. type, etc.). The HW agent metadata model is included in the "description" field in the POST json payload. This field was introduced by us and could have been called hw-agent-metadata or something similar (TBD).

## Create the docker image
```docker-compose build```
## Usage
To start the Flask App that simulates the AIoD API:

```docker-compose up```

To stop a running instance:

```docker compose down```

To test it, simply run the test script (make sure it has execution rights (e.g. **chmod +x test.sh**):

```./test.sh```
