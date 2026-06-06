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

   **Apple Silicon note (M1 / M2 / M3):**

   On Apple Silicon Macs you can run native ARM64 images (recommended) or run x86_64 images under emulation. To detect your Mac's architecture run:

   ```bash
   uname -m
   # returns 'arm64' on Apple Silicon, 'x86_64' on Intel
   ```

   Recommendation:

   - If your Mac reports `arm64`, prefer ARM images (use `--platform linux/arm64` when pulling/running). Many official images now provide ARM builds.
   - If a required image is only available for amd64, Docker Desktop will emulate `linux/amd64` but expect reduced performance and possibly some incompatibilities.

   Examples:

   ```bash
   # Pull native ARM64 image (recommended on Apple Silicon)
   docker pull --platform linux/arm64 osrf/ros:humble-desktop

   # Or pull amd64 image under emulation (slower)
   docker pull --platform linux/amd64 osrf/ros:humble-desktop
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

### Apple Silicon (M1/M2/M3) - Container Setup Notes

If you're on an Apple Silicon Mac (`uname -m` -> `arm64`), prefer pulling and running the ARM64 image to avoid emulation. Use the `--platform linux/arm64` flag when pulling/running the image.

Example (recommended on Apple Silicon):

```bash
# From your project directory
docker pull --platform linux/arm64 osrf/ros:humble-desktop
docker run --platform linux/arm64 -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

If a package or image you need is only available for x86_64, you can run the amd64 image under emulation (slower):

```bash
docker pull --platform linux/amd64 osrf/ros:humble-desktop
docker run --platform linux/amd64 -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

Notes:
- Emulated amd64 containers may be noticeably slower and can have compatibility issues with some native extensions.
- Prefer ARM images where possible; check upstream images or build locally if needed.
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
- **ROS2: Exercise 1 (Pub/Sub)** - Run exercise 1
- **ROS2: Exercise 2 (Services)** - Run exercise 2
- **ROS2: Exercise 3 (Actions)** - Run exercise 3
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


## Apple Silicon Compatibility Notes

Apple Silicon (M1/M2/M3) Macs can run native ARM64 images or run x86_64 images with Docker Desktop emulation. Many core ROS 2 packages work fine on ARM, but some packages that depend on native binary libraries or simulators may require extra work.

Quick checks and recommendations

- Detect architecture:

```bash
uname -m
# 'arm64' on Apple Silicon, 'x86_64' on Intel
```

- Prefer native ARM images when `uname -m` reports `arm64`:

```bash
docker pull --platform linux/arm64 osrf/ros:humble-desktop
docker run --platform linux/arm64 -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

- If a package is only available for amd64, you can fall back to emulation (slower):

```bash
docker pull --platform linux/amd64 osrf/ros:humble-desktop
docker run --platform linux/amd64 -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

Common ROS 2 components that may need attention on Apple Silicon

- Gazebo / Ignition (simulators): official binaries and plugins historically lag for arm64. If you need Gazebo, consider running it on an amd64 VM or using the emulator image and expect possible performance degradation.
- `cv_bridge`, `image_pipeline`, OpenCV-based packages: these rely on OpenCV native libs. On arm64 you may need to install arm64 OpenCV packages or build OpenCV from source inside the container.
- `rosbag2` plugins and compression libraries (lz4, zstd): ensure the compression libraries are available for arm64 or build the plugins from source.
- Packages with native extensions (Cython, C++ nodes with third-party libs): these must be compiled for arm64 inside the container; prebuilt binaries for amd64 will not work.
- `rclpy` / Python bindings: when using the official arm64 ROS image, `rclpy` is typically available via apt inside the container; pip wheels for `rclpy` may not be published for arm64, so prefer the container's apt packages or build from source.

Workarounds and solutions

1. Prefer ARM64 images when possible — much faster than emulation.

2. Build problematic packages from source inside an ARM container:

```bash
# Inside the container in /home/ros2_ws/project
# 1) Place packages in 'src/'
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

3. Use `rosdep` to install missing system dependencies (it will choose the correct architecture when apt repos provide arm64 packages).

```bash
rosdep install --from-paths src --ignore-src -r -y
```

4. If a package depends on a binary third-party library (e.g., OpenCV, Gazebo plugins), install or compile the library for arm64 inside the container before building the ROS package.

5. When a package is not available for arm64 and emulation is tolerable, use `--platform linux/amd64` to run the amd64 image — this is the simplest path but may be slow and occasionally incompatible.

Diagnostic commands

```bash
# Check missing system deps via rosdep
rosdep check --from-paths src --ignore-src -y

# Inspect a built shared object for architecture
file build/<package>/lib/<lib>.so

# Use ldd to list linked libraries
ldd build/<package>/lib/<lib>.so
```

Notes and further reading

- Emulated amd64 containers do not provide accelerated GPU access and will be slower for heavy workloads such as large builds or simulators.
- For complex simulation stacks (Gazebo, Ignition) consider a dedicated amd64 Linux VM or cloud instance if arm64 builds are not available.
- If you frequently target both Intel and Apple Silicon, consider automating a small wrapper script that detects `uname -m` and selects `--platform` accordingly (example below).

Example wrapper (host script) — chooses platform automatically:

```bash
#!/usr/bin/env bash
arch=$(uname -m)
platform=linux/amd64
if [ "$arch" = "arm64" ]; then
   platform=linux/arm64
fi

docker run --platform "$platform" -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

If you want, I can add specific notes for packages you care about (OpenCV/cv_bridge, Gazebo, rosbag2, etc.) with example Dockerfile snippets or build commands.
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
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && python3 test_ros2_setup.py"

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
2. **Verify it works** - Run: `docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && python3 test_ros2_setup.py"`
3. **Use VSCode tasks** - Press Cmd+Shift+B and select a task
4. **Start learning** - Work through tutorials in README

Happy learning! 🐳  🚀
