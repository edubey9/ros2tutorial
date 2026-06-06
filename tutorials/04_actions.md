# Tutorial 4: Actions

Actions are designed for long-running tasks where you need feedback during execution. Unlike services (request-response), actions provide:
- **Goal**: What you want done
- **Feedback**: Progress updates while working
- **Result**: Final outcome

## Use Cases for Actions

- **Robot movement**: Move to a location with progress feedback
- **Manipulation**: Grasp an object with status updates
- **Perception**: Process an image and report intermediate results
- **Any long-running task** that might take seconds or minutes

## Action Structure

An action has three components:

1. **Goal**: Sent by client to server to start the action
2. **Feedback**: Periodic updates from server while working
3. **Result**: Final outcome sent when complete

## Creating an Action Interface

First, let's use a built-in action. We'll use `Fibonacci` action from `action_tutorials_interfaces`.

For this tutorial, we'll simulate using a simple custom goal/result/feedback structure in code.

## Action Server

An Action Server receives goals and works on them, sending feedback periodically and a result when done.

### Simple Action Server Example

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

# For this example, we'll create a simple action interface structure
class CountdownGoal:
    count = 0

class CountdownFeedback:
    current = 0

class CountdownResult:
    final = 0

class MinimalActionServer(Node):
    def __init__(self):
        super().__init__('minimal_action_server')
        self.get_logger().info('Action server created')

    def goal_callback(self, goal_handle):
        """Called when a new goal is received"""
        self.get_logger().info('Received goal request')
        goal = goal_handle.request
        
        # Accept the goal
        goal_handle.succeed()
        
        # Process the goal
        for i in range(goal.count + 1):
            # Send feedback
            feedback = CountdownFeedback()
            feedback.current = i
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Publishing feedback: {i}')
            
            # Simulate work
            rclpy.spin_once(self, timeout_sec=0.1)
        
        # Send final result
        result = CountdownResult()
        result.final = goal.count
        return result

def main(args=None):
    rclpy.init(args=args)
    server = MinimalActionServer()
    rclpy.spin(server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Action Client

An Action Client sends goals and receives feedback and results.

### Simple Action Client Example

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import time

class MinimalActionClient(Node):
    def __init__(self):
        super().__init__('minimal_action_client')
        self.action_client = self.create_action_client(
            Fibonacci,
            'fibonacci'
        )
        
        while not self.action_client.server_is_ready():
            self.get_logger().info('Waiting for action server...')
            time.sleep(1)

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        self._send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.sequence}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = MinimalActionClient()
    action_client.send_goal(10)
    
    # Keep running to receive callbacks
    rclpy.spin(action_client)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Practical Example: Countdown Action

### Action Server (Countdown)

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse
import time

class CountdownActionServer(Node):
    def __init__(self):
        super().__init__('countdown_action_server')
        self._action_server = ActionServer(
            self,
            Countdown,
            'countdown',
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback
        )

    def execute_callback(self, goal_handle):
        """Execute the countdown action"""
        self.get_logger().info(f'Executing countdown from {goal_handle.request.target}')
        
        feedback = Countdown.Feedback()
        
        for i in range(goal_handle.request.target, -1, -1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal cancelled')
                return Countdown.Result()
            
            feedback.current = i
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Countdown: {i}')
            time.sleep(1)
        
        goal_handle.succeed()
        result = Countdown.Result()
        result.complete = True
        return result

    def cancel_callback(self, goal_handle):
        """Called when cancel is requested"""
        return CancelResponse.ACCEPT

def main(args=None):
    rclpy.init(args=args)
    server = CountdownActionServer()
    rclpy.spin(server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Action Client (Countdown)

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

class CountdownActionClient(Node):
    def __init__(self):
        super().__init__('countdown_action_client')
        self._action_client = ActionClient(self, Countdown, 'countdown')

    def send_goal(self, target):
        """Send countdown goal"""
        while not self._action_client.server_is_ready():
            self.get_logger().info('Waiting for countdown action server...')
            time.sleep(1)

        goal_msg = Countdown.Goal()
        goal_msg.target = target

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Current: {feedback_msg.feedback.current}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        self.get_logger().info('Countdown complete!')

def main(args=None):
    rclpy.init(args=args)
    client = CountdownActionClient()
    client.send_goal(5)
    rclpy.spin(client)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Action vs Service vs Publisher/Subscriber

| Feature | Action | Service | Pub/Sub |
|---------|--------|---------|---------|
| Duration | Long-running | Quick | Continuous |
| Feedback | Yes | No | One-way |
| Cancellable | Yes | No | N/A |
| Response Time | Minutes | Seconds | Real-time |
| Use Case | Robot tasks | Queries | Sensors |

## CLI Commands for Actions

```bash
# List all actions
ros2 action list

# Get info about an action
ros2 action info /action_name

# Send a goal via CLI
ros2 action send_goal /countdown Countdown "{target: 5}"

# Send a goal and see feedback
ros2 action send_goal /countdown Countdown "{target: 5}" --feedback
```

## Key Takeaways

1. **Actions are for long-running tasks** with feedback
2. **Actions can be cancelled** by the client
3. **Feedback is published** periodically during execution
4. **Result is sent** when the action completes
5. **Actions are more complex** but provide better UX for long tasks

## Comparison Summary

- **Use Publishers/Subscribers** for continuous data streams
- **Use Services** for quick one-time queries
- **Use Actions** for long-running tasks where you need feedback and cancellation

## Next Steps

Move on to **Tutorial 5: Advanced Topics** to learn about launch files, parameters, and more!
