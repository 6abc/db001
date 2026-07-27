# 🐳 Docker Deployment & Administration Guide

This guide details the standard manual workflow for packaging, tagging, and pushing this repository's source code to Docker Hub, alongside essential administrative reference commands.

---

## 🚀 Manual Build & Push Workflow

Run these commands from the root directory of your local Git repository.

### 1. Authenticate with Registry
Log your terminal session into the Docker Hub registry.
```bash
docker login -u YOUR_DOCKERHUB_USERNAME
```
> ⚠️ **Security Note:** Use a **Personal Access Token (PAT)** instead of your account password when prompted.

### 2. Build the Docker Image
Compile the source code into a container image. The `.` specifies the current directory as the build context.
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/my-app:1.0 .
```

### 3. Tag for Production Environments
Apply the `latest` pointer tag to the specific version build for environment consistency.
```bash
docker tag YOUR_DOCKERHUB_USERNAME/my-app:1.0 YOUR_DOCKERHUB_USERNAME/my-app:latest
```

### 4. Upload to Cloud Registry
Push both the versioned tag and the latest tag to Docker Hub.
```bash
docker push YOUR_DOCKERHUB_USERNAME/my-app:1.0
docker push YOUR_DOCKERHUB_USERNAME/my-app:latest
```

---

## 🛠️ Essential Admin Commands

Use these administrative utilities to monitor, debug, and clean your local Docker environment.

### 📊 Monitoring & Inspection

*   **List Active Containers:** View running containers, IDs, and exposed network ports.
    ```bash
    docker ps
    ```
*   **List All Containers:** View all local containers, including stopped or crashed instances.
    ```bash
    docker ps -a
    ```
*   **List Local Images:** View all downloaded or locally built images and their sizes.
    ```bash
    docker images
    ```
*   **Check Disk Usage:** Inspect how much storage space is consumed by Docker components.
    ```bash
    docker system df
    ```

### 🐛 Debugging & Troubleshooting

*   **Stream Live Logs:** Follow the standard output and error logs of a container in real-time.
    ```bash
    docker logs -f CONTAINER_ID
    ```
*   **Interactive Terminal Shell:** Access the internal file system of an active container.
    ```bash
    docker exec -it CONTAINER_ID sh
    ```

### 🛑 Lifecycle & Deletion

*   **Stop Container:** Gracefully terminate a running container.
    ```bash
    docker stop CONTAINER_ID
    ```
*   **Force Kill Container:** Instantly terminate an unresponsive container.
    ```bash
    docker kill CONTAINER_ID
    ```
*   **Remove Container:** Delete a stopped container instance from storage.
    ```bash
    docker rm CONTAINER_ID
    ```
*   **Remove Image:** Delete an image file from local cache (must not be in use by any container).
    ```bash
    docker rmi IMAGE_ID
    ```

### 🧹 System Pruning & Cleanup

*   **Standard Safe Prune:** Reclaim space by deleting stopped containers, unused networks, and dangling images.
    ```bash
    docker system prune
    ```
*   **Deep System Purge:** Wipe out all unused images, stopped containers, and unreferenced storage volumes.
    ```bash
    docker system prune -a --volumes
    ```
