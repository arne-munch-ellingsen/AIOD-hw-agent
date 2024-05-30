# Mock-up for the AIoD API
We have created a mock-up of the AIoD *computational_asset* API that we can use to create a end-to-end PoC of the cloud native (i.e. Kubernetes) AIoD HW agent. The API has been created using Flask.
## Create the docker image
```docker-compose build```
## Usage
To start the Flask App that simulates the AIoD API:

```docker-compose up```

To stop a running instance:

```docker compose down```

To test it, simply run the test script (make sure it has execution rights (e.g. **chmod +x test.sh**):

```./test.sh```
