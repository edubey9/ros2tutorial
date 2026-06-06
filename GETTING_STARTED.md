# Getting Started with ROS 2

A quick start guide to run the tutorials, examples, and exercises.

## Prerequisites Checklist

- [ ] ROS 2 Humble installed or Docker available
- [ ] Python 3.10+ installed
- [ ] Terminal access
- [ ] Multiple terminal tabs ready

## Step 1: Prepare Your Environment

### For macOS / Windows (Docker recommended):

```bash
# From the project directory, start a ROS 2 container with the
# project mounted at /home/ros2_ws/project (run once):
docker run -it -v "$(pwd):/home/ros2_ws/project" --name ros2-humble osrf/ros:humble-desktop
# Windows PowerShell: use ${PWD} instead of $(pwd)

# Inside the container:
source /opt/ros/humble/setup.bash
cd /home/ros2_ws/project
```

### For Linux:

```bash
# Source ROS 2 setup
source /opt/ros/humble/setup.bash

# Verify installation
ros2 --version
```

## Step 2: Run the Examples

### Example 1: Publisher and Subscriber

**Terminal 1** (Publisher):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/pub_sub_example.py publisher
```

**Terminal 2** (Subscriber):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/pub_sub_example.py subscriber
```

**Expected Output:**
```
Publisher: Publishing: "Hello ROS 2! Message #0"
Subscriber: I heard: "Hello ROS 2! Message #0"
Subscriber: I heard: "Hello ROS 2! Message #1"
...
```

### Example 2: Services

**Terminal 1** (Server):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/service_example.py server
```

**Terminal 2** (Client):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/service_example.py client
```

**Expected Output:**
```
Server: Incoming request: a=2, b=3
Server: Sending back response: 5
Client: Result: 2 + 3 = 5
```

### Example 3: Actions

**Terminal 1** (Server):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/action_example.py server
```

**Terminal 2** (Client):
```bash
cd /home/ros2_ws/project  # or your project path
source /opt/ros/humble/setup.bash
python3 examples/action_example.py client
```

## Step 3: Complete the Exercises

### Exercise 1: Pub/Sub

Use the `exercise_01_pub_sub.py` file and follow the instructions in the comments.

**When finished, run it:**

```bash
# Terminal 1: Publisher
python3 exercises/exercise_01_pub_sub.py pub

# Terminal 2: Subscriber
python3 exercises/exercise_01_pub_sub.py
```

### Exercise 2: Services

Use the `exercise_02_services.py` file and implement the server and client.

**When finished, run it:**

```bash
# Terminal 1: Server
python3 exercises/exercise_02_services.py server

# Terminal 2: Client
python3 exercises/exercise_02_services.py client
```

### Exercise 3: Actions

Use the `exercise_03_actions.py` file and implement the countdown server and client.

**When finished, run it:**

```bash
# Terminal 1: Server
python3 exercises/exercise_03_actions.py server

# Terminal 2: Client
python3 exercises/exercise_03_actions.py client
```

## Useful Debugging Commands

Open a third terminal to monitor what's happening:

```bash
# List running nodes
ros2 node list

# See all topics
ros2 topic list

# Echo a specific topic
ros2 topic echo /chatter

# List services
ros2 service list

# Call a service manually
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"

# View node graph
rqt_graph

# View system logs
rqt_console
```

## Troubleshooting

### "ros2: command not found"
Make sure you source ROS 2:
```bash
source /opt/ros/humble/setup.bash
```

### "Python module not found"
`rclpy` and message packages are **not** pip-installable — they come with ROS 2 itself. If imports fail, it means ROS 2 isn't sourced in this terminal:
```bash
source /opt/ros/humble/setup.bash
```
(If you're on macOS/Windows, make sure you're running the command **inside** the Docker container.)

### "Node cannot communicate"
Check that you're on the same ROS_DOMAIN_ID:
```bash
echo $ROS_DOMAIN_ID  # Should be the same on all terminals
```

### "Service not available"
Make sure the service server is running first, then start the client.

## Learning Path

1. **Read tutorials** in order (01 → 05)
2. **Run examples** while reading
3. **Complete exercises** in order
4. **Experiment**: Modify examples and exercises
5. **Build**: Create your own ROS 2 nodes

## Tips for Success

✅ **Do:**
- Read one tutorial at a time
- Run the corresponding example
- Complete the exercise
- Experiment with changes

❌ **Don't:**
- Try to run multiple examples without reading
- Skip exercises
- Move to advanced topics too quickly
- Get discouraged by errors - they're learning opportunities!

## Next Steps After Exercises

- Create your own package: `ros2 pkg create my_package --build-type ament_python`
- Integrate real sensors
- Explore existing ROS 2 packages
- Build a small robot application
- Join the ROS 2 community: https://discourse.ros.org/

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation.html)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts.html)

---

Happy learning! 🚀
