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

## 🔓 Enable Non-Root User Access (Run on the K3s Server)

By default, the K3s kubeconfig file (`/etc/rancher/k3s/k3s.yaml`) is owned by `root`, so non-root users cannot run `kubectl` commands. To enable permanent access, copy the kubeconfig to your home directory, set the correct ownership and permissions, and configure your shell to use it automatically.

### 1. Create the Kubernetes configuration directory

```bash
mkdir -p ~/.kube
```

### 2. Copy the K3s kubeconfig

```bash
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

### 3. Change ownership to your user

```bash
sudo chown "$(id -u):$(id -g)" ~/.kube/config
```

### 4. Secure the kubeconfig file

```bash
chmod 600 ~/.kube/config
```

### 5. Restore the default Bash configuration (if `.bashrc` is missing)

> **Note:** Skip this step if your `~/.bashrc` already exists and contains your custom shell configuration.

```bash
cp /etc/skel/.bashrc ~/.bashrc
```

### 6. Configure `kubectl` to use the copied kubeconfig permanently

```bash
echo 'export KUBECONFIG=$HOME/.kube/config' >> ~/.bashrc
source ~/.bashrc
```

> **Note:** If you use a shell other than Bash (such as Zsh), add the export command to the appropriate shell configuration file (for example, `~/.zshrc`) instead of `~/.bashrc`.

### 7. Verify the configuration

```bash
echo $KUBECONFIG
kubectl get nodes
```

Expected output:

```text
/home/<your-user>/.kube/config

NAME     STATUS   ROLES           AGE   VERSION
k3cont   Ready    control-plane   ...   ...
```

---

### Troubleshooting

If `kubectl` still attempts to use `/etc/rancher/k3s/k3s.yaml` after completing the steps above:

1. Ensure the environment variable is set:

   ```bash
   echo $KUBECONFIG
   ```

   Expected output:

   ```text
   /home/<your-user>/.kube/config
   ```

2. Confirm the copied kubeconfig exists:

   ```bash
   ls -l ~/.kube/config
   ```

3. If your home directory was created manually and `~/.bashrc` cannot be written, fix its ownership:

   ```bash
   sudo chown -R "$(id -u):$(id -g)" "$HOME"
   ```

4. Start a new terminal session (or log out and back in) and verify:

   ```bash
   kubectl get nodes
   ```

---

## 🔒 Alternative: Configure K3s for Multi-User Access (Optional)

If multiple trusted users need to access the cluster, configure K3s to generate a kubeconfig with readable permissions.

Create or edit the K3s configuration file:

```bash
sudo mkdir -p /etc/rancher/k3s
sudo nano /etc/rancher/k3s/config.yaml
```

Add:

```yaml
write-kubeconfig-mode: "0644"
```

Restart K3s:

```bash
sudo systemctl restart k3s
```

> **Note:** If K3s is running inside a container, restart the container instead of using `systemctl`.

This setting causes `/etc/rancher/k3s/k3s.yaml` to be created with read permissions for all users. For production environments, consider using `0640` with a dedicated group instead of `0644` to limit access.

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

### 4. To make the control-plane only manage the cluster
```bash
kubectl taint nodes k3cont node-role.kubernetes.io/control-plane=true:NoSchedule
```

### 5. If you want the worker nodes to display the worker role
```sh
kubectl label node k3work1 node-role.kubernetes.io/worker=worker
kubectl label node k3work2 node-role.kubernetes.io/worker=worker
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
