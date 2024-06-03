# Install the NVIDIA operator

Installing the NVIDIA GPU Operator to a MicroK8s cluster involves several steps to ensure that your cluster is properly configured to support GPU workloads. Below are the detailed steps to achieve this:

1. **Enable GPU support in MicroK8s:**
   
   First, ensure that your MicroK8s installation supports GPU usage. You can do this by enabling the `gpu` add-on. This will also automatically install NFD and the NVIDIA GPU operator. The NVIDIA GPU operator will set nvidia related NFD labels describing the NVIDIA hardware on the node.

   ```sh
   microk8s enable gpu
   ```

2. **Verify the installation:**

   After the installation, you can verify that the NVIDIA GPU Operator components are running properly.

   ```sh
   microk8s kubectl get pods -n gpu-operator-resources
   ```

   Ensure that all pods are in the `Running` or `Completed` state.

## Optional test deployment of an application that uses a GPU
   You can deploy a sample workload to test the GPU setup. Here’s an example of a CUDA vector addition job:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: cuda-vector-add
   spec:
     restartPolicy: OnFailure
     containers:
       - name: cuda-vector-add
         image: nvidia/samples:vectoradd-cuda10.2
         resources:
           limits:
             nvidia.com/gpu: 1
   ```

   Save this YAML to a file (e.g., `cuda-vector-add.yaml`) and apply it:

   ```sh
   microk8s kubectl apply -f cuda-vector-add.yaml
   ```

   Check the status of the pod:

   ```sh
   microk8s kubectl get pods
   ```

   Once the pod is running, you can view the logs to ensure it executed properly:

   ```sh
   microk8s kubectl logs cuda-vector-add
   ```

These steps should help you successfully install and verify the NVIDIA GPU Operator on your MicroK8s cluster.
