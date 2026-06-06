# ROS 2 Learning Environment

A comprehensive learning project for ROS 2 (Humble) with tutorials and exercises covering publishers, subscribers, services, and actions.

> **💡 For macOS and Windows Users:** ROS 2 natively supports Linux only. The easiest way to get started is using **Docker** (see Docker Setup section below). VSCode integration is available for seamless development.

---

## Quick Setup on a New Computer

### Step 1: Clone the Repository

```bash
# Clone the project to your computer
git clone <repository-url> ros2-learning
cd ros2-learning

# Or if you already have the folder, just ensure it's a git repo:
cd /path/to/ros2tutorial
git status
```

### Step 2: Install ROS 2 Humble

The project requires ROS 2 Humble to be installed on your system. Choose the option that matches your OS:

**⭐ Recommended for macOS and Windows: Use Docker (see Docker Setup section below)**

#### Option A: macOS (Docker - Recommended)

```bash
# Install Docker Desktop: https://www.docker.com/products/docker-desktop

# Then follow the Docker Setup section in this README
# Docker is the easiest and most reliable way to get started!
```

#### Option B: Ubuntu/Debian Linux (Native Installation)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install ROS 2 Humble
sudo apt install -y ros-humble-desktop

# Add to your .bashrc for auto-sourcing
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

#### Option C: Windows 10/11 (Docker - Recommended)

```powershell
# Install Docker Desktop: https://www.docker.com/products/docker-desktop
# (requires the WSL2 backend, which the installer sets up)

# Then follow the Docker Setup section below — all examples and
# exercises run inside the osrf/ros:humble-desktop container.
```

> Alternative: install Ubuntu 22.04 in WSL2 and follow the Linux
> instructions (Option B) inside WSL. Docker is simpler to start with.

---

## Docker Setup for Development (Recommended for macOS and Windows)

Docker allows you to run ROS 2 in a containerized environment without installing it directly on your system. This is the recommended approach for macOS and Windows users.

> **📖 For Complete Docker Documentation:** See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for detailed installation, VSCode integration, task automation, and troubleshooting.

### Docker Installation

#### macOS
```bash
# 1. Download and install Docker Desktop from:
# https://www.docker.com/products/docker-desktop

# 2. Open Docker.app from Applications folder

# 3. Verify installation in terminal
docker --version
docker run hello-world  # Test Docker works
```

#### Windows
```powershell
# 1. Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop

# 2. Run the installer and follow instructions
# Note: May require enabling WSL2 or Hyper-V

# 3. Open PowerShell and verify
docker --version
docker run hello-world  # Test Docker works
```

### Setting Up ROS 2 Docker Container

#### Step 1: Create and Run Container

**macOS:**
```bash
# Navigate to project directory
cd ~/Documents/ros2-learning  # or your project path

# Pull ROS 2 Humble image
docker pull osrf/ros:humble-desktop

# Create container with volume mount (macOS)
docker run -it \
  -v $(pwd):/home/ros2_ws/project \
  --name ros2-humble \
  osrf/ros:humble-desktop /bin/bash

# Inside container, you'll see: root@<container_id>:/#
```

**Windows (PowerShell):**
```powershell
# Navigate to project directory
cd C:\Users\YourUsername\Documents\ros2-learning

# Pull ROS 2 Humble image
docker pull osrf/ros:humble-desktop

# Create container with volume mount (Windows)
docker run -it `
  -v ${PWD}:/home/ros2_ws/project `
  --name ros2-humble `
  osrf/ros:humble-desktop /bin/bash

# Inside container, you'll see: root@<container_id>:/#
```

#### Step 2: Set Up Environment Inside Container

```bash
# Inside the container
source /opt/ros/humble/setup.bash

# Navigate to project
cd /home/ros2_ws/project

# Install Python dependencies (ROS packages are already included)
python3 -m pip install pytest pyyaml

# Verify ROS 2
ros2 --version
```

### Running Commands from Outside the Container

Once your container is running, you can execute commands from your host machine without entering the container.

#### macOS

```bash
# Run a command in the container (from your host terminal)
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Run the test script
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Run an exercise
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py pub"

# Start a bash shell in the container
docker exec -it ros2-humble bash

# After sourcing, you can work interactively
source /opt/ros/humble/setup.bash
```

#### Windows (PowerShell)

```powershell
# Run a command in the container (from your host terminal)
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Run the test script
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Run an exercise
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py pub"

# Start interactive bash shell in the container
docker exec -it ros2-humble bash

# After sourcing, you can work interactively
source /opt/ros/humble/setup.bash
```

### Running From VSCode (Recommended Development Workflow)

#### Setup VSCode Docker Extension

1. **Install Docker Extension in VSCode**
   - Open VSCode
   - Go to Extensions (Cmd+Shift+X on Mac, Ctrl+Shift+X on Windows)
   - Search for "Docker"
   - Install official Docker extension by Microsoft

2. **Verify Container is Running**
   ```bash
   docker ps  # Should show ros2-humble container
   ```

#### Method 1: VSCode Terminal Integration

**macOS/Windows:**
```bash
# In VSCode, open Terminal > New Terminal (Ctrl+`)

# Execute Docker commands to run your Python scripts
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"
```

#### Method 2: VSCode Remote Containers Extension (Advanced)

1. **Install Remote - Containers Extension**
   - Open VSCode Extensions
   - Search for "Remote - Containers"
   - Install it

2. **Attach VSCode to Container**
   - In VSCode, press F1 or Cmd+Shift+P
   - Type: "Remote-Containers: Attach to Running Container"
   - Select "ros2-humble"
   - VSCode will reconnect inside the container

3. **Now you can:**
   - Open integrated terminal - automatically in container
   - Edit files - automatically synced to container
   - Run Python - runs inside container with ROS 2 available
   - Debug - works inside container

#### Method 3: Create Custom VSCode Task

Create `.vscode/tasks.json` in your project:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "ROS2: Run Publisher",
      "type": "shell",
      "command": "docker",
      "args": [
        "exec",
        "-it",
        "ros2-humble",
        "bash",
        "-c",
        "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"
      ],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "ROS2: Run Subscriber",
      "type": "shell",
      "command": "docker",
      "args": [
        "exec",
        "-it",
        "ros2-humble",
        "bash",
        "-c",
        "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py subscriber"
      ],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "ROS2: Run Test Script",
      "type": "shell",
      "command": "docker",
      "args": [
        "exec",
        "-it",
        "ros2-humble",
        "bash",
        "-c",
        "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"
      ],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "ROS2: Run Exercise 1 Publisher",
      "type": "shell",
      "command": "docker",
      "args": [
        "exec",
        "-it",
        "ros2-humble",
        "bash",
        "-c",
        "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py pub"
      ]
    },
    {
      "label": "ROS2: Interactive Bash",
      "type": "shell",
      "command": "docker",
      "args": [
        "exec",
        "-it",
        "ros2-humble",
        "bash"
      ],
      "presentation": {
        "reveal": "always",
        "echo": true
      }
    }
  ]
}
```

**Use the tasks:**
- Press Cmd+Shift+B (Mac) or Ctrl+Shift+B (Windows)
- Select a task from the list
- Task runs in VSCode terminal

### Container Management Commands

#### Start/Stop Container

```bash
# Start existing container
docker start ros2-humble

# Stop container (preserves everything inside)
docker stop ros2-humble

# Check if container is running
docker ps

# See all containers (including stopped)
docker ps -a

# Remove container (deletes it completely)
docker rm ros2-humble

# View container logs
docker logs ros2-humble

# View resource usage
docker stats ros2-humble
```

#### Working with Multiple Terminals

If you need multiple terminals connected to the same container:

```bash
# Terminal 1: Run Publisher
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Terminal 2 (open new terminal): Run Subscriber
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py subscriber"

# Terminal 3 (open new terminal): Run monitoring
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && ros2 topic echo /chatter"
```

### Docker Tips and Tricks

#### Permanent Shell Configuration

To avoid sourcing ROS 2 each time, add it to container's `.bashrc`:

```bash
# Run once
docker exec ros2-humble bash -c "echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc"

# Now all future commands have ROS 2 sourced automatically
docker exec -it ros2-humble bash
# ROS 2 is already available!
```

#### Share Files Between Host and Container

Your project folder is already mounted at `/home/ros2_ws/project`:

```bash
# Edit files on your host computer
# They instantly appear in container at /home/ros2_ws/project

# Example: Edit from macOS terminal
nano ~/Documents/ros2-learning/exercises/exercise_01_pub_sub.py

# File is immediately available in container
docker exec ros2-humble bash -c "cat /home/ros2_ws/project/exercises/exercise_01_pub_sub.py"
```

### Docker Troubleshooting

**Problem: "Docker daemon is not running"**
```bash
# macOS: Start Docker Desktop app
open -a Docker

# Windows: Start Docker Desktop app from Start menu
```

**Problem: "Container already exists"**
```bash
# Remove the old container
docker rm ros2-humble

# Create a new one
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash
```

**Problem: "Cannot connect to docker socket"**
```bash
# macOS: Restart Docker
killall Docker
open -a Docker

# Windows: Restart Docker Desktop from system tray
```

**Problem: "Volume mount not working"**
```bash
# macOS: Ensure Docker has file sharing enabled
# Settings > Resources > File Sharing > Add your project directory

# Windows: Ensure WSL2 backend is enabled
# Settings > General > Use WSL2 based engine
```

---

### Step 3: Set Up Python Environment

```bash
# Navigate to project directory
cd /path/to/ros2-learning

# Create virtual environment (optional)
# IMPORTANT: --system-site-packages is required, or the venv will
# hide the ROS 2 packages (rclpy etc.) and imports will fail!
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check ROS 2
ros2 --version

# Check Python packages
python3 -c "import rclpy; print('✓ rclpy installed')"

# Run a quick test
python3 examples/pub_sub_example.py publisher &
sleep 2
python3 examples/pub_sub_example.py subscriber &
sleep 5
pkill -f "pub_sub_example"
```

## Prerequisites

- **ROS 2 Humble** installed on your system (see [Quick Setup](#quick-setup-on-a-new-computer))
- **Python 3.10+**
- **pip** package manager
- **Git** (for cloning and version control)

## Resetting Your Environment

### If ROS 2 Services Aren't Working

```bash
# Clear ROS 2 daemon
ros2 daemon stop
ros2 daemon status

# Clear any stale connections
pkill -f rclpy
pkill -f ros2
```

### If You Need to Reinstall Python Dependencies

```bash
# Remove old virtual environment
rm -rf venv

# Create fresh virtual environment (--system-site-packages keeps
# the ROS 2 packages visible inside the venv)
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Full Environment Reset (If Everything is Broken)

```bash
# Docker users
docker stop ros2-humble
docker rm ros2-humble
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash

# Linux users
source /opt/ros/humble/setup.bash
ros2 daemon stop
pkill -f ros2
# Then re-run your nodes
```

### Verify Your Setup Works

```bash
# Quick verification script
python3 -c "
import rclpy
from std_msgs.msg import String
from example_interfaces.srv import AddTwoInts
from action_tutorials_interfaces.action import Fibonacci
print('✓ All imports successful')
print('✓ ROS 2 is properly configured')
"
```

## Project Structure

```
.
├── README.md                      # This file
├── GETTING_STARTED.md             # Quick start guide
├── DOCKER_GUIDE.md                # Docker setup and VSCode integration
├── FRESH_SETUP.md                 # New-computer setup guide
├── PROGRESS_TRACKER.md            # Learning progress tracking
├── requirements.txt               # Python dependencies
├── test_ros2_setup.py             # Python test script
├── test_setup.sh                  # Bash test script
├── .vscode/tasks.json             # VSCode tasks (run examples via Docker)
├── tutorials/                     # Learning materials
│   ├── 01_setup.md
│   ├── 02_publisher_subscriber.md
│   ├── 03_services.md
│   ├── 04_actions.md
│   └── 05_advanced_topics.md
├── examples/                      # Working code examples
│   ├── pub_sub_example.py
│   ├── service_example.py
│   └── action_example.py
└── exercises/                     # Hands-on exercises
    ├── exercise_01_pub_sub.py
    ├── exercise_02_services.py
    └── exercise_03_actions.py
```

## Setup

1. **Clone/navigate to the project**:
   ```bash
   cd /path/to/ros2tutorial   # inside Docker: /home/ros2_ws/project
   ```

2. **Install Python dependencies** (if using native ROS 2):
   ```bash
   pip install -r requirements.txt
   ```

3. **Source ROS 2 setup** (for native installation):
   ```bash
   source /opt/ros/humble/setup.bash
   ```

## Tutorial Outline

### How to Work Through the Tutorials

Follow this structured learning path:

1. **Read the tutorial** markdown file completely
2. **Read the associated code example** in `examples/` folder
3. **Run the example** using the provided instructions
4. **Complete the corresponding exercise** in `exercises/` folder
5. **Verify your work** using the test scripts below
6. **Move to the next tutorial** only after exercises work

#### Tutorial 1: Setup (`01_setup.md`)
**Time: 30 minutes**
- Understand ROS 2 concepts (nodes, topics, services, actions)
- Learn the node lifecycle
- Run your first ROS 2 node
- **No exercise** - focus on understanding concepts

#### Tutorial 2: Publishers and Subscribers (`02_publisher_subscriber.md`)
**Time: 1-2 hours**
- Create your first publisher
- Create your first subscriber
- Understand asynchronous communication
- **Exercise 1**: Build a counter publisher/subscriber
- **Test**: Run both simultaneously and verify message flow

#### Tutorial 3: Services (`03_services.md`)
**Time: 1-2 hours**
- Create service servers
- Create service clients
- Understand synchronous request-response
- **Exercise 2**: Build a multiplication service
- **Test**: Call the service multiple times from client

#### Tutorial 4: Actions (`04_actions.md`)
**Time: 1.5-2 hours**
- Understand goals, feedback, and results
- Implement action servers and clients
- Handle long-running tasks
- **Exercise 3**: Build a countdown action
- **Test**: Send goals and observe feedback

#### Tutorial 5: Advanced Topics (`05_advanced_topics.md`)
**Time: 2-3 hours**
- Parameters and configuration
- Launch files for multi-node systems
- Debugging tools and commands
- Optional: Lifecycle nodes, rosbags, Docker

### Estimated Total Time: 6-10 hours

## Test Scripts and Verification

### Automated Test Scripts

Two test scripts are included in the repository:

```bash
# Python version (recommended)
python3 test_ros2_setup.py
python3 test_ros2_setup.py --verify    # Quick check only

# Bash version
bash test_setup.sh
```

The test scripts check:
- ✓ Python packages installed correctly
- ✓ ROS 2 properly installed and accessible
- ✓ All tutorial, example, and exercise files present
- ✓ Basic pub/sub communication works

### Manual Testing Checklist

After completing each tutorial/exercise, verify with this checklist:

#### Exercise 1: Publisher/Subscriber
- [ ] Publisher node runs without errors
- [ ] Subscriber node connects to publisher
- [ ] Messages appear in subscriber with correct format
- [ ] Test with `ros2 topic echo /counter`

```bash
# Test commands
ros2 node list                    # Should show both nodes
ros2 topic list                   # Should show /counter
ros2 topic echo /counter          # Should show messages
```

#### Exercise 2: Services
- [ ] Service server starts and waits for requests
- [ ] Service client connects to server
- [ ] Correct results returned from service
- [ ] Test multiple requests work

```bash
# Test commands
ros2 service list                 # Should show /multiply_numbers
ros2 service type /multiply_numbers  # Should show example_interfaces/srv/AddTwoInts
ros2 service call /multiply_numbers example_interfaces/srv/AddTwoInts "{a: 5, b: 6}"  # Should return 30 (if multiplying)
```

#### Exercise 3: Countdown Action
- [ ] Action server starts
- [ ] Client sends goal successfully
- [ ] Feedback messages appear during countdown
- [ ] Final result is received

```bash
# Monitor with
ros2 node list                    # Should show both nodes
ros2 action list                  # Should show /countdown
# Check logs for feedback messages
```

### Learning Verification Questions

After each tutorial, test your understanding:

**Tutorial 1 - Setup:**
- [ ] Can you explain what a node is?
- [ ] What's the difference between topics, services, and actions?
- [ ] How do you run a ROS 2 node?

**Tutorial 2 - Pub/Sub:**
- [ ] How do you create a publisher in ROS 2?
- [ ] What's the QoS parameter for?
- [ ] Can you explain why pub/sub is asynchronous?
- [ ] How would you create a subscriber for Int32 messages?

**Tutorial 3 - Services:**
- [ ] What's the difference between pub/sub and services?
- [ ] How does a client know when the service is available?
- [ ] What happens if a service call fails?

**Tutorial 4 - Actions:**
- [ ] How are actions different from services?
- [ ] What are the three components of an action?
- [ ] When would you use an action instead of a service?

**Tutorial 5 - Advanced:**
- [ ] How do you pass parameters to a node?
- [ ] What's the purpose of a launch file?
- [ ] Name two ROS 2 debugging tools you learned about

### Running Examples

Each example can be run in separate terminal windows:

```bash
# Example 1: Publisher/Subscriber
# Terminal 1 (Publisher)
python3 examples/pub_sub_example.py publisher

# Terminal 2 (Subscriber)
python3 examples/pub_sub_example.py subscriber
```

```bash
# Example 2: Service Server/Client
# Terminal 1 (Server)
python3 examples/service_example.py server

# Terminal 2 (Client)
python3 examples/service_example.py client
```

```bash
# Example 3: Action Server/Client
# Terminal 1 (Server)
python3 examples/action_example.py server

# Terminal 2 (Client)
python3 examples/action_example.py client
```

## Exercises

Complete the exercises in order to reinforce your learning. Each exercise includes:
- Clear challenge description
- TODO comments marking what to implement
- Hints for implementation
- Expected behavior

### Exercise Workflow

1. **Open the exercise file** in your editor
2. **Read all TODO comments** to understand what needs implementation
3. **Compare with the example** in the examples/ folder
4. **Implement the missing code**
5. **Test in two terminals** using the provided test commands
6. **Verify the output** matches expected behavior
7. **Move to next exercise** only after success

### Exercise 1: Publisher/Subscriber Counter
**File:** `exercises/exercise_01_pub_sub.py`

**What to implement:**
```python
# Create PublisherNode class
# - Create a publisher for Int32 messages on 'counter' topic
# - Create a timer that publishes 0-10 sequentially
# - Publish one message per second

# Create SubscriberNode class
# - Subscribe to 'counter' topic
# - Log each received number
```

**Test it:**
```bash
# Terminal 1
python3 exercises/exercise_01_pub_sub.py pub

# Terminal 2
python3 exercises/exercise_01_pub_sub.py
```

**Expected output:**
```
Terminal 1: Publishing: 0, Publishing: 1, ...
Terminal 2: Received: 0, Received: 1, ...
```

### Exercise 2: Multiplication Service
**File:** `exercises/exercise_02_services.py`

**What to implement:**
```python
# Create MultiplyServer class
# - Create a service server for 'multiply_numbers'
# - Multiply request.a * request.b
# - Return result in response.sum

# Create MultiplyClient class
# - Create a service client for 'multiply_numbers'
# - Wait for service to be available
# - Send requests with different number pairs
```

**Test it:**
```bash
# Terminal 1
python3 exercises/exercise_02_services.py server

# Terminal 2
python3 exercises/exercise_02_services.py client
```

**Expected output:**
```
Server: Incoming request: a=3, b=4
Server: Sending back response: 12
Client: Result: 3 * 4 = 12
```

### Exercise 3: Countdown Action
**File:** `exercises/exercise_03_actions.py`

**What to implement:**
```python
# Create CountdownServer class
# - Create an ActionServer named 'countdown' (reusing the Fibonacci interface)
# - In execute_callback: count down from goal.order to 0
# - Publish each step as feedback with goal_handle.publish_feedback()
# - Mark the goal succeeded and return the full sequence as the result

# Create CountdownClient class
# - Create an ActionClient named 'countdown'
# - Send a goal with send_goal_async(), registering a feedback callback
# - Display feedback as it arrives, then print the final result
```

**Test it:**
```bash
# Terminal 1
python3 exercises/exercise_03_actions.py server

# Terminal 2
python3 exercises/exercise_03_actions.py client
```

**Expected output:**
```
Server: Countdown: 5, 4, 3, 2, 1, 0 ... Goal succeeded
Client: Feedback: [5], [5, 4], ... Result: [5, 4, 3, 2, 1, 0]
```

### Common Exercise Mistakes

| Mistake | Solution |
|---------|----------|
| "ImportError: No module named rclpy" | Source ROS 2: `source /opt/ros/humble/setup.bash` (run inside the container on macOS/Windows) |
| "Service not available" | Make sure server runs BEFORE client |
| Node doesn't connect | Check topic/service names match exactly |
| Messages not printing | Verify callback function is named correctly |
| Timeout errors | Check ROS_DOMAIN_ID is same in all terminals |

## Useful Commands

```bash
# List all running nodes
ros2 node list

# List all topics
ros2 topic list

# Echo a topic
ros2 topic echo /topic_name

# List all services
ros2 service list

# Call a service
ros2 service call /service_name std_srvs/srv/Empty

# List all actions
ros2 action list

# Get node information
ros2 node info /node_name

# Get topic information
ros2 topic info /topic_name
```

## Troubleshooting Guide

### Installation Issues

**Problem: "ros2: command not found"**
```bash
# Solution: Source ROS 2 setup
source /opt/ros/humble/setup.bash

# Or add to ~/.bashrc for automatic sourcing:
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**Problem: "Cannot find Python module rclpy"**
```bash
# rclpy is NOT pip-installable — it ships with ROS 2 itself.
# Solution: source ROS 2 in this terminal
source /opt/ros/humble/setup.bash

# On macOS/Windows, make sure you're running the command INSIDE
# the Docker container (docker exec -it ros2-humble bash)
```

**Problem: "ModuleNotFoundError" when running exercises**
```bash
# Make sure you're in the project directory
cd /path/to/ros2-learning

# Activate virtual environment if you're using one
source venv/bin/activate

# Then run the script
python3 exercises/exercise_01_pub_sub.py
```

### Runtime Issues

**Problem: "Service not available" after waiting**
```bash
# This means the service server isn't running
# Solution: Start the server FIRST, then the client

# Terminal 1 (Server)
python3 examples/service_example.py server

# Wait for it to print "Service ready..."
# Then in Terminal 2 (Client)
python3 examples/service_example.py client
```

**Problem: Nodes can't communicate**
```bash
# Check if nodes are visible
ros2 node list

# If nodes don't show up, reset ROS 2 daemon
ros2 daemon stop
ros2 daemon status

# Kill any stuck processes
pkill -f rclpy
pkill -f ros2

# Try again
```

**Problem: "Timeout waiting for service"**
```bash
# Multiple terminals need same ROS_DOMAIN_ID
echo $ROS_DOMAIN_ID

# If empty, that's normal (default is 0)
# If different across terminals, set it same:
export ROS_DOMAIN_ID=0
```

**Problem: Messages not being received**
```bash
# Monitor the topic in a new terminal
ros2 topic echo /topic_name

# If nothing appears, publisher isn't running
# If data appears, subscriber callback might be wrong

# Check node info
ros2 node info /subscriber_node_name
ros2 node info /publisher_node_name

# Verify they're on same topic
ros2 topic info /topic_name
```

### Exercise-Specific Issues

**Exercise 1 Not Working**
```bash
# Verify Int32 is being used
ros2 topic echo /counter  # Should show std_msgs/msg/Int32 data

# Check the publisher is looping
# Should see "Publishing" messages in first terminal
```

**Exercise 2 Not Working**
```bash
# Test the service manually
ros2 service call /multiply_numbers example_interfaces/srv/AddTwoInts "{a: 5, b: 6}"

# Should return sum (or in your case, product)
# If not, server implementation is wrong
```

**Exercise 3 Not Working**
```bash
# Check for countdown feedback
# Server terminal should show counting down
# Client terminal should receive and display feedback
```

### Docker-Specific Issues

**Problem: Can't mount volume in Docker**
```bash
# Make sure Docker is running
docker ps

# If permissions denied, add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Try mounting again
docker run -it -v $(pwd):/home/ros2_ws/project osrf/ros:humble-desktop /bin/bash
```

**Problem: Changes inside container aren't saved**
```bash
# Always mount a volume to persist changes
# Bad:
docker run -it osrf/ros:humble-desktop /bin/bash

# Good:
docker run -it -v $(pwd):/home/ros2_ws/project osrf/ros:humble-desktop /bin/bash

# Now edit files in /home/ros2_ws/project and they persist
```

### Performance Issues

**Problem: ROS 2 running slowly**
```bash
# Check for stuck daemons
ps aux | grep ros2
ps aux | grep rclpy

# Kill stuck processes
pkill -9 -f ros2
pkill -9 -f rclpy

# Restart
ros2 daemon stop
```

### Getting Help

If you're stuck:

1. **Check the error message carefully** - it usually tells you what's wrong
2. **Read the tutorial again** - the concepts section explains this
3. **Compare with the example** - see how it's done correctly
4. **Check the comments** - tutorials have detailed comments
5. **Use debugging commands** - `ros2 node list`, `ros2 topic echo`, etc.
6. **Search online** - ROS 2 has great community documentation

## Version Control and Git Setup

### Setting Up on a New Computer from Git

```bash
# Clone the repository
git clone <your-repo-url> ros2-learning
cd ros2-learning

# Verify all files are present
ls -la tutorials/ examples/ exercises/

# Install dependencies
pip install -r requirements.txt

# Run the test script to verify setup
python3 test_ros2_setup.py
```

### Git Workflow

```bash
# Check status
git status

# After modifying exercise files, track changes
git add exercises/

# Commit your progress
git commit -m "Completed Exercise 1: Publisher/Subscriber"

# Push to remote
git push origin main

# On another computer, pull your progress
git pull origin main
```

### Creating a New Git Repository

If you don't have a repository yet:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial ROS 2 learning environment setup"

# Add remote (GitHub example)
git remote add origin https://github.com/username/ros2-learning.git

# Push to remote
git push -u origin main
```

## Using the Progress Tracker

The **PROGRESS_TRACKER.md** file helps you track your learning:

```bash
# Open the progress tracker
cat PROGRESS_TRACKER.md
```

Features:
- ✓ Checkboxes for each section
- ✓ Time estimates for each tutorial
- ✓ Knowledge verification questions
- ✓ Exercise completion checklist
- ✓ Personal reflection space
- ✓ Self-assessment scoring

## Quick Reference

### Essential Directory Structure

```
.
├── README.md                      # Main documentation
├── GETTING_STARTED.md             # Quick start guide
├── DOCKER_GUIDE.md                # Docker setup and VSCode integration
├── FRESH_SETUP.md                 # New-computer setup guide
├── PROGRESS_TRACKER.md            # Learning progress tracking
├── test_ros2_setup.py            # Python test script
├── test_setup.sh                 # Bash test script
├── requirements.txt               # Python dependencies
├── .vscode/tasks.json             # VSCode tasks (run examples via Docker)
│
├── tutorials/                     # 5 learning tutorials
│   ├── 01_setup.md              # Concepts and setup
│   ├── 02_publisher_subscriber.md # Pub/Sub pattern
│   ├── 03_services.md           # Service pattern
│   ├── 04_actions.md            # Action pattern
│   └── 05_advanced_topics.md    # Advanced topics
│
├── examples/                      # Working code examples
│   ├── pub_sub_example.py       # Publisher/Subscriber example
│   ├── service_example.py       # Service server/client example
│   └── action_example.py        # Action server/client example
│
└── exercises/                     # Practice exercises
    ├── exercise_01_pub_sub.py    # Ex1: Publisher/Subscriber
    ├── exercise_02_services.py   # Ex2: Services
    └── exercise_03_actions.py    # Ex3: Actions
```

### Quick Start Commands

```bash
# Verify installation
python3 test_ros2_setup.py

# Run examples
python3 examples/pub_sub_example.py publisher
python3 examples/pub_sub_example.py subscriber

# Test communication in real-time
ros2 topic list
ros2 topic echo /topic_name
ros2 node list
```

### Docker Quick Reference

**For macOS and Windows Users (Using Docker):**

```bash
# Setup (one time)
docker pull osrf/ros:humble-desktop
docker run -it -v $(pwd):/home/ros2_ws/project --name ros2-humble osrf/ros:humble-desktop /bin/bash

# Run commands without entering container (macOS/Windows)
docker exec ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 test_ros2_setup.py"

# Run examples
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 examples/pub_sub_example.py publisher"

# Run exercises
docker exec -it ros2-humble bash -c "source /opt/ros/humble/setup.bash && cd /home/ros2_ws/project && python3 exercises/exercise_01_pub_sub.py"

# Start interactive shell in container
docker exec -it ros2-humble bash

# Container management
docker start ros2-humble      # Start stopped container
docker stop ros2-humble       # Stop container
docker ps                     # List running containers
docker logs ros2-humble       # View container logs
```

**VSCode Integration (Recommended):**

1. Install Docker extension in VSCode
2. Use tasks in `.vscode/tasks.json` (already provided in project)
3. Run tasks with Cmd+Shift+B (Mac) or Ctrl+Shift+B (Windows)
4. See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for advanced VSCode setup

## Resources

### Official Documentation
- [ROS 2 Official Site](https://www.ros.org/)
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts.html)
- [ROS 2 Design](https://design.ros2.org/)

### Learning Resources
- [ROS 2 GitHub](https://github.com/ros2/ros2)
- [ROS 2 Examples](https://github.com/ros2/examples)
- [ROS Discourse (Q&A)](https://discourse.ros.org/)
- [ROS 2 YouTube Tutorials](https://www.youtube.com/results?search_query=ros2+tutorial)

### Tools and Utilities
- [RQT GUI Tools](https://github.com/ros-visualization/rqt)
- [ROS 2 Command Line Tools](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html)
- [ROS 2 Security](https://docs.ros.org/en/humble/Tutorials/Advanced/Security/Security.html)

### Community
- [ROS Discourse](https://discourse.ros.org/) - Ask questions
- [ROS Answers](https://answers.ros.org/) - Q&A site
- [GitHub Issues](https://github.com/ros2/ros2/issues) - Report bugs
