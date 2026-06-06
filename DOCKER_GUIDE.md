# Docker Setup Guide for ROS 2 Learning Environment

This guide covers everything you need to know about using Docker with the ROS 2 learning environment on macOS and Windows.

## Table of Contents

1. [Installation](#installation)
2. [Container Setup](#container-setup)
3. [Running Commands](#running-commands)
4. [VSCode Integration](#vscode-integration)
5. [Tips and Tricks](#tips-and-tricks)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- **macOS**: Mac with Apple Silicon (M1/M2/M3) or Intel processor
- **Windows**: Windows 10 Pro/Enterprise or Windows 11

### Docker Desktop Installation

#### macOS

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Choose version for your Mac (Apple Silicon or Intel)

2. **Install**
   - Open the downloaded `.dmg` file
   - Drag Docker.app to Applications folder
   - Wait for installation to complete

3. **Launch Docker**
   - Open Applications folder
   - Double-click Docker.app
   - Enter your password if prompted
   - Wait for Docker menu icon to appear in top menu bar

4. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world  # Should print "Hello from Docker!"
   ```

#### Windows (PowerShell)

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"

2. **Install**
   - Run the installer
   - Follow the setup wizard
   - Accept the service agreement
   - Choose installation options
   - Click "Install"

3. **Post-Installation**
   - Restart your computer when prompted
   - Docker will start automatically
   - Look for Docker icon in system tray

4. **Verify Installation**
   ```powershell
   docker --version
   docker run hello-world
   ```

---

## Container Setup

### Creating ROS 2 Humble Container

This is a one-time setup process.

#### macOS

```bash
# Navigate to your project directory
cd ~/Documents/ros2-learning  # Or wherever you cloned it

# Pull the ROS 2 Humble image (first time only, ~2GB)
docker pull osrf/ros:humble-desktop

# Create and run container with volume mount
docker run -it \
  -v $(pwd):/home/ros2_ws/project \
  --name ros2-humble \
  osrf/ros:humble-desktop /bin/bash

# NOTE for Apple Silicon (M1/M2/M3) Macs: the osrf/ros image is
# amd64-only, so add --platform linux/amd64 before -v (it runs
# under emulation; slower but works):
# docker run -it --platform linux/amd64 -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

**You're now inside the container!** You should see: `root@<container_id>:/#`

```bash
# Inside the container - verify ROS 2
source /opt/ros/humble/setup.bash
ros2 --version

# Navigate to project
cd /home/ros2_ws/project

# Install development packages
python3 -m pip install pytest pyyaml

# Exit container (but keep it running)
exit
```

#### Windows (PowerShell)

```powershell
# Navigate to your project directory
cd C:\Users\YourUsername\Documents\ros2-learning

# Pull the ROS 2 Humble image (first time only, ~2GB)
docker pull osrf/ros:humble-desktop

# Create and run container with volume mount
docker run -it `
  -v ${PWD}:/home/ros2_ws/project `
  --name ros2-humble `
  osrf/ros:humble-desktop /bin/bash
```

**You're now inside the container!** You should see: `root@<container_id>:/#`

```bash
# Inside the container - verify ROS 2
source /opt/ros/humble/setup.bash
ros2 --version

# Navigate to project
cd /home/ros2_ws/project

# Install development packages
python3 -m pip install pytest pyyaml

# Exit container (but keep it running)
exit
```

---

## Running Commands

### Method 1: From Host Terminal (Easiest)

No need to enter the container. Run commands directly from your Mac/Windows terminal.

#### macOS

```bash
# Test the setup
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Run a publisher example
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Run an exercise
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py pub"
```

#### Windows (PowerShell)

```powershell
# Test the setup
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Run a publisher example
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Run an exercise
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py pub"
```

### Method 2: Inside Container Shell

For interactive work or if you need multiple commands.

#### macOS/Windows

```bash
# Enter the container (interactive shell)
docker exec -it ros2-humble bash

# Inside container, source ROS 2 (one time per session)
source /opt/ros/humble/setup.bash

# Now you can run commands directly
python3 examples/pub_sub_example.py publisher
ros2 --version
ros2 topic list

# To exit: Ctrl+D or type 'exit'
```

### Method 3: Multiple Terminals for Pub/Sub

Need multiple terminals? Open several host terminals and run in each:

**Terminal 1 (Publisher):**
```bash
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"
```

**Terminal 2 (Subscriber):**
```bash
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py subscriber"
```

**Terminal 3 (Monitor):**
```bash
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && ros2 topic echo /chatter"
```

---

## VSCode Integration

### Quick Setup (Recommended)

1. **Install Docker Extension**
   - Open VSCode
   - Cmd+Shift+X (Mac) or Ctrl+Shift+X (Windows)
   - Search: "Docker"
   - Install "Docker" by Microsoft

2. **Use Pre-built Tasks**
   - Open `.vscode/tasks.json` file (already created in project)
   - Press Cmd+Shift+B (Mac) or Ctrl+Shift+B (Windows)
   - Select a task to run (e.g., "ROS2: Run Publisher")
   - Task output appears in VSCode terminal

### Available Tasks

The project includes these pre-configured tasks:

- **ROS2: Run Test Script** - Verify your setup
- **ROS2: Run Publisher (Example 1)** - Run pub/sub publisher
- **ROS2: Run Subscriber (Example 1)** - Run pub/sub subscriber
- **ROS2: Run Service Server (Example 2)** - Run service server
- **ROS2: Run Service Client (Example 2)** - Run service client
- **ROS2: Run Action Server (Example 3)** - Run action server
- **ROS2: Run Action Client (Example 3)** - Run action client
- **ROS2: Exercise 1 Publisher / Subscriber** - Run exercise 1 (run both, in two tasks)
- **ROS2: Exercise 2 Server / Client** - Run exercise 2 (start Server first)
- **ROS2: Exercise 3 Server / Client** - Run exercise 3 (start Server first)
- **ROS2: Interactive Container Shell** - Open bash in container
- **ROS2: Start Docker Container** - Start the container
- **ROS2: Stop Docker Container** - Stop the container
- **ROS2: Check Container Status** - List all containers

### Advanced: Remote Containers Extension

For an even more integrated experience:

1. **Install Remote - Containers Extension**
   - Open VSCode Extensions
   - Search: "Remote - Containers"
   - Install by Microsoft

2. **Attach to Container**
   - Press F1 or Cmd+Shift+P
   - Type: "Remote-Containers: Attach to Running Container"
   - Select "ros2-humble"

3. **Now:**
   - VSCode terminal runs inside container
   - File edits sync automatically
   - Run Python directly
   - Debug works inside container
   - Install extensions inside container

---

## Tips and Tricks

### 1. Make Bash Permanent

Avoid sourcing ROS 2 every time:

```bash
# Run once
docker exec ros2-humble bash -c "echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc"

# Now all future commands have ROS 2 ready
docker exec -it ros2-humble bash
# ROS 2 is already sourced!
```

### 2. Edit Files from Host

Your project folder is synced in the container:

```bash
# Edit on your Mac/Windows (file appears in container instantly)
nano ~/Documents/ros2-learning/exercises/exercise_01_pub_sub.py

# File available in container at:
docker exec ros2-humble bash -c "ls -la /home/ros2_ws/project/exercises/"
```

### 3. Copy Files To/From Container

```bash
# Copy from host to container
docker cp ~/file.txt ros2-humble:/home/ros2_ws/project/

# Copy from container to host
docker cp ros2-humble:/home/ros2_ws/project/output.txt ~/
```

### 4. Inspect Container

```bash
# View container logs
docker logs ros2-humble

# Check container resource usage
docker stats ros2-humble

# Detailed container info
docker inspect ros2-humble
```

### 5. Using Aliases (macOS/Linux)

Add to your `~/.bash_profile` or `~/.zshrc`:

```bash
# Quick commands
alias docker-ros2="docker exec -it ros2-humble bash"
alias docker-pub="docker exec -it ros2-humble bash -c \"source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher\""
alias docker-sub="docker exec -it ros2-humble bash -c \"source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py subscriber\""

# Usage: Just type 'docker-ros2' to enter container
```

---

## Troubleshooting

### Container Issues

**"Docker daemon is not running"**
```bash
# macOS: Start Docker Desktop
open -a Docker

# Windows: Start from Start menu or system tray
```

**"Container already exists"**
```bash
# Remove old container
docker rm ros2-humble

# Create new one
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

**"Cannot connect to docker socket"**
```bash
# macOS: Restart Docker
killall Docker
sleep 2
open -a Docker

# Windows: Restart Docker Desktop from system tray
```

### Volume Mount Issues

**"Cannot mount volume"**
```bash
# macOS: Check Docker file sharing settings
# Docker Menu > Settings > Resources > File Sharing
# Make sure ~/Documents is in the list

# Windows: Enable WSL2 backend
# Docker Desktop > Settings > General > Use WSL 2 based engine
```

**"Files not syncing between host and container"**
```bash
# Check mount is working
docker exec ros2-humble bash -c "ls -la /home/ros2_ws/project"

# Should show your project files

# If not, recreate container:
docker rm ros2-humble
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

### Performance Issues

**"Container running slowly"**
```bash
# Check container resource limits
docker stats ros2-humble

# Increase Docker resource limits:
# Docker Menu > Settings > Resources > Memory/CPU
# Increase allocated resources and restart Docker
```

**"Slow file operations in mounted volume"**
```bash
# This is normal on Docker Desktop
# Consider copying large files into container:
docker cp ~/large_file.zip ros2-humble:/home/ros2_ws/project/
```

### Command Issues

**"Command not found in container"**
```bash
# Make sure to source ROS 2
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && ros2 --version"

# Or make it permanent (see Tips section)
```

**"Python import errors"**
```bash
# Reinstall packages
docker exec ros2-humble bash -c "python3 -m pip install pytest pyyaml"

# Or rebuild container
docker rm ros2-humble
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

### Getting Help

If something doesn't work:

1. Check Docker is running (`docker ps` should work)
2. Verify container exists (`docker ps -a | grep ros2`)
3. Check container logs (`docker logs ros2-humble`)
4. Check file permissions (`docker exec ros2-humble bash -c "ls -la /home/ros2_ws/project"`)
5. Try restarting Docker (close Docker Desktop, reopen)
6. Search the error on Docker documentation

---

## Quick Reference Card

```bash
# Setup (one time)
docker pull osrf/ros:humble-desktop
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash

# Run commands without entering container
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Enter interactive shell
docker exec -it ros2-humble bash

# Container management
docker start ros2-humble      # Start container
docker stop ros2-humble       # Stop container
docker ps                     # List running containers
docker ps -a                  # List all containers
docker logs ros2-humble       # View logs
docker rm ros2-humble         # Delete container
docker stats ros2-humble      # Resource usage
```

---

## Next Steps

1. **Set up container** - Follow Container Setup section above
2. **Verify it works** - Run: `docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"`
3. **Use VSCode tasks** - Press Cmd+Shift+B and select a task
4. **Start learning** - Work through tutorials in README

Happy learning! 🐳  🚀
