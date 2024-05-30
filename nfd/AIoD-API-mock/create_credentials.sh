#!/bin/bash

# Create a service account
microk8s kubectl create serviceaccount aiod-user

# Bind the service account to the cluster-admin role
microk8s kubectl create clusterrolebinding aiod-user-binding --clusterrole=cluster-admin --serviceaccount=default:my-user

# Get the secret name associated with the service account
SECRET_NAME=$(microk8s kubectl get serviceaccount aiod-user -o jsonpath='{.secrets[0].name}')

# Retrieve the token
TOKEN=$(microk8s kubectl get secret $SECRET_NAME -o jsonpath='{.data.token}' | base64 --decode)

# Display the token
echo "Your token is: $TOKEN"
