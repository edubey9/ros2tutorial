# Tutorial 1: ROS 2 Setup and Concepts

## What is ROS 2?

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

## Key Concepts

### 1. **Nodes**
A node is an executable that uses ROS to communicate with other nodes. Think of it as a process in your system that does a specific job.

Example:
- A sensor driver node reads data from a sensor
- A processing node transforms that data
- A control node sends commands to actuators

### 2. **Topics**
Topics are buses over which nodes exchange messages. A node can *publish* data to a topic or *subscribe* to a topic to receive data. This is a one-way, asynchronous communication pattern.

Example:
- A camera node publishes images to `/camera/image` topic
- A vision processing node subscribes to `/camera/image` topic

### 3. **Services**
Services are a synchronous request-response mechanism between nodes. One node (service client) makes a request, and another node (service server) provides a response.

Example:
- A trajectory planner requests a service to compute an inverse kinematics solution
- A kinematics solver service calculates and returns the joint angles

### 4. **Actions**
Actions are for long-running tasks with feedback. A node sends a goal to an action server, which works on it and periodically sends feedback, then returns a result.

Example:
- A move robot action: client sends goal position, server sends feedback about progress, then returns final position reached

### 5. **Messages**
Messages are the data structures used for communication between nodes. ROS 2 uses standardized message types.

Common message types:
- `std_msgs/String`: A simple string message
- `std_msgs/Int32`: An integer message
- `geometry_msgs/Twist`: Velocity commands (linear and angular)
- `sensor_msgs/Image`: Image data from a camera

## Creating Your First Node

Here's a minimal ROS 2 node that prints a message:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Minimal node started!')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Node Lifecycle

1. **Initialization** (`rclpy.init()`): Initialize the ROS 2 Python client
2. **Node Creation**: Create your node instance
3. **Spinning** (`rclpy.spin()`): Keep the node running and processing callbacks
4. **Shutdown** (`rclpy.shutdown()`): Clean up resources

## Running a Node

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Run your node
python3 your_node.py
```

## Useful ROS 2 CLI Commands

```bash
# List all running nodes
ros2 node list

# Get information about a specific node
ros2 node info /node_name

# List all available topics
ros2 topic list

# Get information about a topic
ros2 topic info /topic_name

# View topic data in real-time
ros2 topic echo /topic_name

# Publish a message to a topic (for testing)
ros2 topic pub /topic_name std_msgs/String "data: 'hello'"
```

## Next Steps

Now that you understand the basic concepts, move on to **Tutorial 2: Publishers and Subscribers** to learn how to send and receive data between nodes.
