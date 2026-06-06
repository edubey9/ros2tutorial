#!/usr/bin/env python3
"""
Exercise 3: Actions

Challenge: Create a REAL action server and client for a countdown.
           The server counts down from a target number, publishing
           feedback at each step. The client sends the goal and prints
           feedback as it arrives.

We reuse the Fibonacci action interface (included with ROS 2 Humble desktop)
so we don't need to build a custom interface package:

    # Goal
    int32 order              <- we use this as the countdown start value
    ---
    # Result
    int32[] sequence         <- we return the full countdown, e.g. [5,4,3,2,1,0]
    ---
    # Feedback
    int32[] partial_sequence <- we publish the countdown so far at each step

Instructions:
1. Implement CountdownServer
   - Create an ActionServer for the 'countdown' action
   - In execute_callback: count down from goal.order to 0
   - Append each number to feedback.partial_sequence and publish it
   - Sleep 1 second between numbers
   - Mark the goal succeeded and return the full sequence as the result

2. Implement CountdownClient
   - Create an ActionClient for the 'countdown' action
   - Wait for the server, send a goal, and register callbacks
   - Print feedback messages as they arrive
   - Print the final result

3. Run server in one terminal, client in another:
   - Terminal 1: python exercises/exercise_03_actions.py server
   - Terminal 2: python exercises/exercise_03_actions.py client

Hints:
- Compare with examples/action_example.py — the structure is identical,
  only the computation differs (countdown instead of Fibonacci)
- Server: ActionServer(self, Fibonacci, 'countdown', execute_callback=...)
- Server: goal_handle.publish_feedback(feedback_msg), goal_handle.succeed()
- Client: send_goal_async(goal_msg, feedback_callback=...) returns a future;
  add a done-callback to get the goal handle, then call get_result_async()
- Check goal_handle.is_cancel_requested inside the loop for bonus credit

Expected output:
    Server: Counting down: 5, 4, 3, 2, 1, 0 ... Goal succeeded
    Client: Feedback: [5], [5, 4], [5, 4, 3], ... Result: [5, 4, 3, 2, 1, 0]
"""

import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient
from action_tutorials_interfaces.action import Fibonacci


# TODO: Implement CountdownServer class
# - Constructor should create an ActionServer named 'countdown'
# - execute_callback should count down and publish feedback
class CountdownServer(Node):
    def __init__(self):
        super().__init__('countdown_server')
        # TODO: Create the ActionServer
        # self._action_server = ActionServer(self, Fibonacci, 'countdown',
        #                                    execute_callback=self.execute_callback)
        self.get_logger().info('Countdown server ready')

    def execute_callback(self, goal_handle):
        """Count down from goal_handle.request.order to 0"""
        # TODO: Implement countdown logic
        # - Create a Fibonacci.Feedback() message
        # - Loop from goal_handle.request.order down to 0:
        #     - Append the current number to feedback.partial_sequence
        #     - Publish feedback with goal_handle.publish_feedback(...)
        #     - Log the current number
        #     - time.sleep(1)
        # - Call goal_handle.succeed()
        # - Return a Fibonacci.Result() containing the full sequence
        pass


# TODO: Implement CountdownClient class
# - Constructor should create an ActionClient named 'countdown'
# - send_goal should send the goal and register feedback/result callbacks
class CountdownClient(Node):
    def __init__(self):
        super().__init__('countdown_client')
        # TODO: Create the ActionClient
        # self._action_client = ActionClient(self, Fibonacci, 'countdown')

    def send_goal(self, target):
        """Send a countdown goal for the given target number"""
        # TODO: Implement request logic
        # - Wait for the server: self._action_client.wait_for_server()
        # - Create a Fibonacci.Goal() and set goal.order = target
        # - Send it with send_goal_async(goal, feedback_callback=self.feedback_callback)
        # - Add a done-callback to handle the server's accept/reject response
        pass

    def feedback_callback(self, feedback_msg):
        # TODO: Log feedback_msg.feedback.partial_sequence
        pass

    def goal_response_callback(self, future):
        # TODO: Get the goal handle, check goal_handle.accepted,
        #       then request the result with get_result_async()
        pass

    def get_result_callback(self, future):
        # TODO: Log future.result().result.sequence, then rclpy.shutdown()
        pass


def main():
    rclpy.init()

    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        node = CountdownServer()
        print("Starting Countdown Server...")
        print("Waiting for client goals")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
        node.destroy_node()
        rclpy.shutdown()
    else:
        node = CountdownClient()
        print("Starting Countdown Client...")
        node.send_goal(5)
        try:
            # Spins until get_result_callback calls rclpy.shutdown()
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == '__main__':
    main()
