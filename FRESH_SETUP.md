# Fresh Installation Guide - New Computer Setup

This guide walks you through setting up the ROS 2 learning environment on a completely new computer from scratch.

## Total Time Required: 30-60 minutes (varies by OS and internet speed)

---

## Step 1: Clone the Repository (5 minutes)

### Prerequisites
- Git installed on your computer
- Access to the repository (GitHub, GitLab, etc.)

### Commands

```bash
# Navigate to where you want the project
cd ~/Projects  # or any directory you prefer

# Clone the repository
git clone <repository-url> ros2-learning

# Navigate into the project
cd ros2-learning

# Verify files are present
ls -la
# You should see: README.md, tutorials/, examples/, exercises/, requirements.txt, test_*.py, test_*.sh
```

---

## Step 2: Install ROS 2 Humble (15-30 minutes)

Choose your operating system:

### macOS Users (Docker Recommended)

```bash
# 1. Install Docker (if not already installed)
# Visit: https://www.docker.com/products/docker-desktop
# Follow installation instructions

# 2. Verify Docker installation
docker --version

# 3. Pull ROS 2 Humble image
docker pull osrf/ros:humble-desktop

# 4. Create a container with the project mounted
docker run -it -v $(pwd):/home/ros2_ws/project \
    --name ros2-humble \
    osrf/ros:humble-desktop /bin/bash

# 5. Inside the container:
source /opt/ros/humble/setup.bash
cd /home/ros2_ws/project
```

**Note**: Every time you want to work, use:
```bash
docker start ros2-humble
docker exec -it ros2-humble bash
```

### Ubuntu/Debian Linux Users

```bash
# 1. Update system packages
sudo apt update
sudo apt upgrade -y

# 2. Add ROS 2 repository
sudo apt install -y curl gnupg2 lsb-release ubuntu-keyring
curl -sSL https://repo.ros2.org/ros.key | sudo apt-key add -

# 3. Install ROS 2 Humble
sudo apt install -y ros-humble-desktop

# 4. Add to shell startup
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 5. Verify installation
ros2 --version
```

### Windows 10/11 Users (WSL2)

```bash
# 1. Install Windows Subsystem for Linux 2
# Follow: https://learn.microsoft.com/en-us/windows/wsl/install

# 2. Install Ubuntu 22.04 LTS from Microsoft Store

# 3. Open Ubuntu terminal and follow Linux instructions above
```

---

## Step 3: Set Up Python Environment (5 minutes)

```bash
# Navigate to project directory (if not already there)
cd ~/Projects/ros2-learning

# Create virtual environment (optional but recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows (WSL):
source venv/Scripts/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 4: Verify Installation (5 minutes)

```bash
# Run the test script to verify everything
python3 test_ros2_setup.py

# Or bash version:
bash test_setup.sh
```

### Expected Output

You should see:
```
✓ Python packages are installed
✓ ROS 2 is installed
✓ Tutorial files verified
✓ Example files verified
✓ Exercise files verified
✓ Pub/Sub communication working

🎉 All checks passed! You're ready to start learning ROS 2!
```

If any check fails, see the **Troubleshooting** section below.

---

## Step 5: Take Your First Steps (5 minutes)

```bash
# Source ROS 2 (if using native Linux, already done)
source /opt/ros/humble/setup.bash

# Run the first example - Terminal 1
cd ~/Projects/ros2-learning
python3 examples/pub_sub_example.py publisher

# In a new terminal, activate environment and run - Terminal 2
source /opt/ros/humble/setup.bash
cd ~/Projects/ros2-learning
python3 examples/pub_sub_example.py subscriber
```

You should see messages flowing from publisher to subscriber!

---

## Troubleshooting Fresh Setup

### Problem: "ros2: command not found"

**Solution:**
```bash
# Make sure you sourced ROS 2
source /opt/ros/humble/setup.bash

# Add to your shell startup file permanently:
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# For zsh users:
echo "source /opt/ros/humble/setup.bash" >> ~/.zshrc
source ~/.zshrc
```

### Problem: "ModuleNotFoundError: No module named 'rclpy'"

**Solution:**
```bash
# Reinstall Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python3 -c "import rclpy; print('✓ rclpy installed')"
```

### Problem: "Permission denied" when running scripts

**Solution:**
```bash
# Make scripts executable
chmod +x test_setup.sh
chmod +x examples/*.py
chmod +x exercises/*.py

# Run tests
bash test_setup.sh
```

### Problem: Docker errors

**Solution:**
```bash
# Check Docker is running
docker ps

# If "Cannot connect to Docker daemon":
# Start Docker application (macOS: open -a Docker)

# Check container status
docker ps -a

# Start existing container
docker start ros2-humble
docker exec -it ros2-humble bash
```

### Problem: Virtual environment not activating

**Solution:**
```bash
# Verify venv exists
ls -la venv/

# If missing, recreate it
python3 -m venv venv

# Make sure you're in the project directory
cd ~/Projects/ros2-learning

# Activate (macOS/Linux)
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

---

## Next: Start Learning

Once you've verified everything works:

1. **Read the README.md** for complete documentation
2. **Open GETTING_STARTED.md** for detailed instructions
3. **Start with tutorials/01_setup.md** - work through in order
4. **Use PROGRESS_TRACKER.md** to track your progress

---

## Git Workflow for Syncing Between Computers

### On Computer 1: Complete Exercise
```bash
cd ~/Projects/ros2-learning

# Make changes to exercises
# ... edit exercise_01_pub_sub.py ...

# Commit your work
git add exercises/
git commit -m "Completed Exercise 1: Publisher/Subscriber"

# Push to remote
git push origin main
```

### On Computer 2: Get Latest Changes
```bash
cd ~/Projects/ros2-learning

# Pull latest changes
git pull origin main

# Verify you got the changes
ls -la exercises/
```

---

## Common Setup Mistakes to Avoid

❌ **Don't**: Skip sourcing ROS 2 setup
✓ **Do**: Always source the setup script in new terminals

❌ **Don't**: Run examples without installing dependencies
✓ **Do**: Run `pip install -r requirements.txt` first

❌ **Don't**: Forget to run the test script
✓ **Do**: Run `python3 test_ros2_setup.py` after setup

❌ **Don't**: Run subscriber before publisher
✓ **Do**: Always start publisher/server first, then subscriber/client

❌ **Don't**: Skip the tutorials and jump to exercises
✓ **Do**: Read each tutorial completely before doing the exercise

---

## Environment Setup Reference

### Important Environment Variables

```bash
# Check ROS 2 home
echo $ROS_HOME
# Usually: ~/.ros

# Check ROS domain ID (should be same across terminals)
echo $ROS_DOMAIN_ID
# Empty is fine (defaults to 0)

# View all ROS-related variables
printenv | grep -i ros
```

### Making Setup Permanent

**macOS/Linux (.bashrc or .zshrc):**
```bash
# Add to ~/.bashrc or ~/.zshrc
source /opt/ros/humble/setup.bash
```

**Activate virtual environment automatically:**
```bash
# Add to ~/.bashrc
cd ~/Projects/ros2-learning && source venv/bin/activate
```

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.10+ |
| Disk Space | 2 GB | 5 GB |
| RAM | 2 GB | 4 GB+ |
| Network | 1 MB/s | 10 MB/s+ |

---

## Getting Help

If something goes wrong:

1. **Read the error message carefully** - it usually tells you the issue
2. **Check the main README.md** troubleshooting section
3. **Run the test script** to identify which component failed
4. **Compare with examples** to see working code
5. **Search online** for the specific error message
6. **Ask the community** on ROS Discourse

---

## You're Ready! 🚀

Once you've completed this setup:
- All required software is installed
- All files are present and readable
- Communication between nodes is working
- You're ready to start the tutorials!

**Next Step**: Open `tutorials/01_setup.md` and begin learning ROS 2!

Happy coding! 😊
