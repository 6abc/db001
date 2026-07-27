# ☸️ K3s Kubernetes Cluster Administration Guide

This guide details the end-to-end process for installing a lightweight K3s cluster (Master and Worker nodes), setting up non-root user permissions, and essential operational commands.

---

## 🏗️ Cluster Architecture & Installation

### 1. Master Node Installation
Run this command on your designated primary server to initialize the control plane.
```bash
curl -sfL https://get.k3s.io | sh -
```
Verify the master node is running and operational:
```bash
sudo kubectl get nodes
```
Extract the unique cluster join token required for connecting worker nodes:
```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

### 🔓 Enable Non-Root User Access (Run on Master Node)
By default, K3s requires root permissions to access the cluster configuration. Run these steps to allow standard users to run `kubectl` commands without prefixing `sudo`.

1. **Create the local config directory:**
   ```bash
   mkdir -p \$HOME/.kube
   ```
2. **Copy the cluster configuration file:**
   ```bash
   sudo cp /etc/rancher/k3s/k3s.yaml \$HOME/.kube/config
   ```
3. **Change ownership of the configuration file to your user:**
   ```bash
   sudo chown \$(id -u):\((id -g)\)HOME/.kube/config
   ```
4. **Secure the file permissions:**
   ```bash
   chmod 600 \$HOME/.kube/config
   ```
5. **Set the environment variable (Optional, adds persistence):**
   ```bash
   echo "export KUBECONFIG=\$HOME/.kube/config" >> ~/.bashrc
   source ~/.bashrc
   ```

*(Note: All subsequent `kubectl` commands below can now be run without `sudo`)*

### 2. Worker Node Installation
Run this command on each background server you wish to join to the cluster. Replace placeholders with your master node's local IP address and the token extracted above.
```bash
curl -sfL https://k3s.io | K3S_URL=https://<MASTER_NODE_IP>:6443 K3S_TOKEN=<MASTER_NODE_TOKEN> sh -
```

### 3. Verify the Completed Cluster
Return to your **Master Node** and execute this command to confirm all infrastructure nodes have registered successfully and transitioned into a `Ready` state.
```bash
kubectl get nodes -o wide
```

---

## 🚀 Basic Cluster Operations

Run these commands on your master node or from a configured local machine to check cluster health.

### 1. Monitor Application Resources
List deployments, active running pods, services, and network entry points across all environments.
```bash
kubectl get all -A
```

### 2. Track Cluster Event Logs
View the real-time system ledger to debug scheduling issues, failures, or resource constraints.
```bash
kubectl get events -A --sort-by='.metadata.creationTimestamp'
```

---

## 🛠️ Application Deployment (CLI & Manifests)

### 1. Apply Manifest Configurations
Deploy infrastructure configurations, network rules, or applications using YAML files.
```bash
kubectl apply -f deployment.yaml
```

### 2. Quick Test Deployment
Spin up a quick internal application image directly from the command line interface without a file.
```bash
kubectl create deployment temporary-app --image=YOUR_DOCKERHUB_USERNAME/my-app:latest
```

### 3. Delete Resources Cleanly
Remove application deployments and their underlying workloads from the cluster.
```bash
kubectl delete -f deployment.yaml
# Or by resource name:
kubectl delete deployment temporary-app
```

---

## 🐛 Debugging & Deep Inspection

### 1. Read Workload Logs
Stream application log outputs from a specific pod to troubleshoot internal application errors.
```bash
kubectl logs -f POD_NAME -n NAMESPACE
```

### 2. Inspect Detailed Resource State
View the low-level system configuration, environment states, and failure histories of a resource.
```bash
kubectl describe pod POD_NAME -n NAMESPACE
```

### 3. Execute Interactive Container Shell
Drop directly into the terminal of a running pod to run local test scripts or verify network paths.
```bash
kubectl exec -it POD_NAME -n NAMESPACE -- sh
```

---

## 📊 Performance, Scale & Metrics

### 1. Check Real-Time Resource Usage
Monitor physical CPU and RAM consumption across nodes or individual active pods.
```bash
kubectl top nodes
kubectl top pods -A
```

### 2. Scale Application Replicas
Instantly adjust the running instance count of a targeted application workload up or down.
```bash
kubectl scale deployment/my-app --replicas=3
```

---

## 🛑 K3s Engine Control (Host Node Commands)

*System control commands still require administrative privileges (`sudo`) because they manage the core host OS daemon.*

*   **Restart K3s Master Engine (Master Only):** Reload the controller manager without interrupting underlying host operations.
    ```bash
    sudo systemctl restart k3s
    ```
*   **Restart K3s Agent Engine (Worker Only):** Restart the local runtime daemon on a worker machine.
    ```bash
    sudo systemctl restart k3s-agent
    ```
*   **Stop All Workloads & Engine:** Cleanly shut down all orchestration routines on the local host.
    ```bash
    sudo systemctl stop k3s        # Run on Master
    sudo systemctl stop k3s-agent  # Run on Worker
    ```
