# Close the CPU gap
This folder contains an example kubernetes app (pod) that retireves the missing values for:
* number of physical cpus
* CPU model name
* CPU clockspeed

## Build and deploy the app
```
# Build container and import into microk8s containerd
docker build -t local/nfd-cpu-labeler:latest .
docker save local/nfd-cpu-labeler:latest -o nfd-cpu-labeler.tar
microk8s.ctr images import nfd-cpu-labeler.tar

# Deploy
microk8s.kubectl apply -f deployment.yaml
```
## Check logs and tags
```
# Get the name of the deployed pod
microk8s kubectl get pods

# Check log (substitute the pod name with the name from the get pods command above
kubectl logs nfd-cpu-labeler-55d4b574c9-kmqws
```
You can also check the NFD labels using this command
*microk8s kubectl get nodes -o json*
