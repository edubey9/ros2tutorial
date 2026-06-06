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

## Action Interfaces

Unlike topics and services, an action's goal/feedback/result structure is defined in a `.action` interface file that must be compiled into a package — you **cannot** use plain Python classes for this.

For this tutorial we use the `Fibonacci` action from `action_tutorials_interfaces`, which ships with the ROS 2 Humble desktop installation (including the `osrf/ros:humble-desktop` Docker image):

```
# Fibonacci.action
# Goal
int32 order
---
# Result
int32[] sequence
---
# Feedback
int32[] partial_sequence
```

```python
from action_tutorials_interfaces.action import Fibonacci
```

(Creating your own `.action` interface requires a custom interface package — see the official docs: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)

## Action Server

An Action Server receives goals and works on them, sending feedback periodically and a result when done.

```python
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,            # action type
            'fibonacci',          # action name
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback,
        )

    def cancel_callback(self, goal_handle):
        """Called when the client requests cancellation"""
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Do the work: publish feedback as we go, then return the result"""
        self.get_logger().info(f'Executing goal: Fibonacci({goal_handle.request.order})')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            # Stop early if the client cancelled the goal
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            )
            goal_handle.publish_feedback(feedback_msg)   # send progress to client
            time.sleep(0.5)                              # simulate long-running work

        # Only mark the goal succeeded AFTER the work is done
        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    server = FibonacciActionServer()
    rclpy.spin(server)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Key points:
- `ActionServer(...)` registers the server on the ROS graph — without it, nothing is reachable by clients.
- `goal_handle.publish_feedback(...)` streams progress to the client during execution.
- `goal_handle.succeed()` is called **after** the work completes (not to "accept" the goal — acceptance is automatic unless you provide a `goal_callback`).

## Action Client

An Action Client sends goals and receives feedback and results. The flow is asynchronous and callback-driven:

1. `send_goal_async()` → future resolves with a **goal handle** (accepted/rejected)
2. `goal_handle.get_result_async()` → future resolves with the **result**
3. `feedback_callback` fires every time the server publishes feedback

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        # Block until the server is available
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {list(feedback.partial_sequence)}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {list(result.sequence)}')
        rclpy.shutdown()   # we're done — stop spinning


def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)

    # Keep running to receive callbacks (until get_result_callback shuts down)
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
```

## Try It: Run the Example

The working version of this code is in `examples/action_example.py`:

```bash
# Terminal 1
python3 examples/action_example.py server

# Terminal 2
python3 examples/action_example.py client
```

You should see feedback arriving in the **client** terminal while the **server** computes — that's the key behavior that distinguishes actions from services.

## Adapting It: Countdown

Exercise 3 asks you to build a countdown action. You can reuse the same `Fibonacci` interface — treat `goal.order` as the number to count down from, and publish the countdown-so-far as `partial_sequence`. The server skeleton:

```python
def execute_callback(self, goal_handle):
    feedback_msg = Fibonacci.Feedback()

    for i in range(goal_handle.request.order, -1, -1):
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return Fibonacci.Result()

        feedback_msg.partial_sequence.append(i)
        goal_handle.publish_feedback(feedback_msg)
        self.get_logger().info(f'Countdown: {i}')
        time.sleep(1)

    goal_handle.succeed()
    result = Fibonacci.Result()
    result.sequence = feedback_msg.partial_sequence
    return result
```

The client is identical to the Fibonacci client — only the action name changes.

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
ros2 action info /fibonacci

# Send a goal via CLI
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}"

# Send a goal and see feedback
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}" --feedback
```

## Key Takeaways

1. **Actions are for long-running tasks** with feedback
2. **Actions can be cancelled** by the client
3. **Feedback is published** periodically during execution
4. **Result is sent** when the action completes
5. **Action interfaces are compiled `.action` files**, not plain Python classes
6. **`goal_handle.succeed()` comes after the work**, not before

## Comparison Summary

- **Use Publishers/Subscribers** for continuous data streams
- **Use Services** for quick one-time queries
- **Use Actions** for long-running tasks where you need feedback and cancellation

## Next Steps

Move on to **Tutorial 5: Advanced Topics** to learn about launch files, parameters, and more!
