# Tutorial 2: Publishers and Subscribers

Publishers and Subscribers are the core communication pattern in ROS 2. This is asynchronous, one-way communication perfect for continuous data streams.

## Publisher

A Publisher sends messages to a topic. Multiple publishers can publish to the same topic.

### Simple Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Create a publisher that publishes String messages to the 'topic' topic
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        
        # Create a timer that calls the timer_callback every 0.5 seconds
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Subscriber

A Subscriber receives messages from a topic. Multiple subscribers can listen to the same topic.

### Simple Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        # Create a subscriber that listens to the 'topic' topic
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # This function is called whenever a new message arrives
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Understanding the Code

### QoS (Quality of Service)

The number `10` in `create_publisher()` and `create_subscription()` is the QoS queue size:
- `10`: Keep the last 10 messages in the queue
- Higher values: More memory but tolerance for slower subscribers
- Lower values: Less memory but may miss messages

### Timer Callback

```python
self.timer = self.create_timer(timer_period, self.timer_callback)
```

This creates a timer that calls `timer_callback()` every `timer_period` seconds. Useful for periodic tasks.

### Message Callback

```python
def listener_callback(self, msg):
```

This is called automatically whenever a new message arrives on the subscribed topic.

## Common Message Types

### String Message
```python
from std_msgs.msg import String
msg = String()
msg.data = "Hello"
```

### Integer Message
```python
from std_msgs.msg import Int32
msg = Int32()
msg.data = 42
```

### Float Message
```python
from std_msgs.msg import Float32
msg = Float32()
msg.data = 3.14
```

## Running Publisher and Subscriber

Terminal 1 (Publisher):
```bash
source /opt/ros/humble/setup.bash
python publisher_node.py
```

Terminal 2 (Subscriber):
```bash
source /opt/ros/humble/setup.bash
python subscriber_node.py
```

Terminal 3 (Optional - Monitor):
```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /topic
```

## Practical Example: Sensor Data

### Publisher (Sensor Simulator)
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperatureSensor(Node):
    def __init__(self):
        super().__init__('temperature_sensor')
        self.publisher_ = self.create_publisher(Float32, 'temperature', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.base_temp = 20.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.base_temp + random.uniform(-1.0, 1.0)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing temperature: {msg.data:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    sensor = TemperatureSensor()
    rclpy.spin(sensor)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber (Temperature Monitor)
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureMonitor(Node):
    def __init__(self):
        super().__init__('temperature_monitor')
        self.subscription = self.create_subscription(
            Float32,
            'temperature',
            self.listener_callback,
            10
        )
        self.high_temp_threshold = 25.0

    def listener_callback(self, msg):
        temp = msg.data
        if temp > self.high_temp_threshold:
            self.get_logger().warn(f'High temperature alert! {temp:.2f}°C')
        else:
            self.get_logger().info(f'Temperature: {temp:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    monitor = TemperatureMonitor()
    rclpy.spin(monitor)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Key Takeaways

1. **Publishers send data** to a topic at any frequency
2. **Subscribers listen** to a topic and react when data arrives
3. **Multiple publishers and subscribers** can use the same topic
4. **This pattern is asynchronous** - publishers don't wait for subscribers
5. **Timers are useful** for periodic tasks

## Next Steps

Now that you understand pub/sub, move on to **Tutorial 3: Services** to learn about synchronous request-response communication.
