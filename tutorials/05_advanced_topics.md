# Tutorial 5: Advanced Topics

This tutorial covers more advanced ROS 2 concepts to take your skills to the next level.

## 1. Parameters

Parameters are configuration values that nodes can read and update at runtime.

### Setting Parameters

```python
import rclpy
from rclpy.node import Node

class ParameterExample(Node):
    def __init__(self):
        super().__init__('parameter_example')
        
        # Declare parameters with default values
        self.declare_parameter('my_parameter', 'default_value')
        self.declare_parameter('update_rate', 1.0)
        
        # Get parameter values
        my_param = self.get_parameter('my_parameter').value
        rate = self.get_parameter('update_rate').value
        
        self.get_logger().info(f'Parameter value: {my_param}')
        self.get_logger().info(f'Update rate: {rate}')

def main(args=None):
    rclpy.init(args=args)
    node = ParameterExample()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Using Parameters from Command Line

```bash
# Run with custom parameter values
ros2 run my_package my_node --ros-args -p my_parameter:='custom_value' -p update_rate:=2.0
```

### Monitoring Parameters

```bash
# List all parameters for a node
ros2 param list

# Get a specific parameter
ros2 param get /node_name my_parameter

# Set a parameter
ros2 param set /node_name my_parameter new_value
```

## 2. Launch Files

Launch files allow you to start multiple nodes with one command and set their parameters.

### Simple Launch File (XML format)

Create `launch/my_launch.launch.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<launch>
    <!-- Start node 1 -->
    <node pkg="my_package" exec="node1" name="node1_instance">
        <param name="update_rate" value="10"/>
    </node>
    
    <!-- Start node 2 -->
    <node pkg="my_package" exec="node2" name="node2_instance">
        <param name="topic_name" value="/sensor_data"/>
    </node>
    
    <!-- Remap topic names -->
    <node pkg="my_package" exec="node3" name="node3_instance">
        <remap from="input_topic" to="processed_data"/>
    </node>
</launch>
```

### Launch File in Python

Create `launch/my_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='node1',
            name='node1_instance',
            parameters=[{'update_rate': 10}]
        ),
        Node(
            package='my_package',
            executable='node2',
            name='node2_instance',
            parameters=[{'topic_name': '/sensor_data'}]
        ),
        Node(
            package='my_package',
            executable='node3',
            name='node3_instance',
            remappings=[('input_topic', 'processed_data')]
        ),
    ])
```

### Running a Launch File

```bash
# Run XML launch file
ros2 launch my_package my_launch.launch.xml

# Run Python launch file
ros2 launch my_package my_launch.py
```

## 3. Lifecycle Nodes

Lifecycle nodes follow a state machine: unconfigured → inactive → active → finalized

### Lifecycle Node Example

```python
import rclpy
from rclpy.lifecycle import Node
from rclpy.lifecycle import State
from rclpy.lifecycle import TransitionCallbackReturn

class LifecycleExample(Node):
    def __init__(self):
        super().__init__('lifecycle_example')

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        """Called when transitioning to 'configuring' state"""
        self.get_logger().info('Configuring...')
        # Initialize resources here
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        """Called when transitioning to 'activating' state"""
        self.get_logger().info('Activating...')
        # Start publishers, subscribers, timers
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        """Called when transitioning to 'deactivating' state"""
        self.get_logger().info('Deactivating...')
        # Stop publishers, subscribers, timers
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        """Called when transitioning to 'unconfiguring' state"""
        self.get_logger().info('Cleaning up...')
        # Release resources
        return TransitionCallbackReturn.SUCCESS

def main(args=None):
    rclpy.init(args=args)
    node = LifecycleExample()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Transitioning Lifecycle States

```bash
# List lifecycle nodes
ros2 lifecycle nodes

# Get current state
ros2 lifecycle get /node_name

# Transition to configure
ros2 lifecycle set /node_name configure

# Transition to activate
ros2 lifecycle set /node_name activate

# Transition to deactivate
ros2 lifecycle set /node_name deactivate

# Transition to cleanup
ros2 lifecycle set /node_name cleanup
```

## 4. Recording and Playing Back Data (ROS 2 Bags)

ROS 2 bags record topic messages for later playback and analysis.

### Recording Data

```bash
# Record all topics
ros2 bag record -a

# Record specific topics
ros2 bag record /topic1 /topic2

# Record with output directory
ros2 bag record -a -o my_bag_file
```

### Playing Back Data

```bash
# Play back a recording
ros2 bag play my_bag_file

# Play at different speed
ros2 bag play my_bag_file --rate 2.0

# Loop playback
ros2 bag play my_bag_file --loop
```

### Analyzing Bags

```bash
# Get info about a bag
ros2 bag info my_bag_file
```

## 5. Debugging and Troubleshooting

### Using ROS 2 CLI Tools

```bash
# List all active nodes
ros2 node list

# Get detailed node info
ros2 node info /node_name

# List all topics
ros2 topic list

# Echo topic data with type info
ros2 topic echo /topic_name --no-arr

# Check service calls
ros2 service list
ros2 service type /service_name

# Debug node graph
ros2 run rqt_graph rqt_graph

# View node relationships
rqt_graph
```

### Using RQT Tools

RQT provides GUI tools for debugging:

```bash
# Launch RQT console (see all logging output)
rqt_console

# View topics in real-time
rqt_topic

# Plot numeric topic data
rqt_plot /topic_name/field

# Service caller GUI
rqt_service_caller
```

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Nodes can't find each other | Check `ROS_DOMAIN_ID` environment variable |
| Messages not being received | Use `ros2 topic echo` to verify data is published |
| Service not found | Ensure service server is running and uses correct name |
| High latency | Check QoS settings, reduce message frequency |

## 6. Docker Integration

Run ROS 2 in Docker for reproducibility:

### Dockerfile

```dockerfile
FROM osrf/ros:humble-desktop

# Install additional packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your code
COPY . .

# Source ROS 2
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["/bin/bash"]
```

### Running Docker Container

```bash
# Build image
docker build -t my-ros2-app .

# Run container
docker run -it my-ros2-app

# Run with volume mount (for live code editing)
docker run -it -v $(pwd):/app my-ros2-app
```

## Key Takeaways

1. **Parameters** make nodes configurable at runtime
2. **Launch files** simplify starting multiple nodes
3. **Lifecycle nodes** provide controlled startup/shutdown
4. **Rosbags** allow recording and replaying data
5. **RQT tools** provide visual debugging
6. **Docker** ensures reproducibility across environments

## Next Steps

- Build your own ROS 2 package
- Integrate with real sensors
- Deploy on a robot
- Join the ROS 2 community!

---

Congratulations on completing the tutorials! You now have a solid understanding of ROS 2 fundamentals.
