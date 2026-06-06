#!/usr/bin/env python3
"""
Exercise 3: Actions (Simplified)

Challenge: Create an action that counts down from a number,
           sending feedback as it counts down.

Instructions:
1. Create a Countdown Server node
   - Goal: Target number to count down from
   - Feedback: Current count
   - Result: Completed (True/False)

2. Create a Countdown Client node
   - Send a goal to count down from 10
   - Print feedback messages as they arrive
   - Print the final result

3. This is a simplified version without a custom action interface
   - We'll demonstrate the concepts with timers and logging

Hints:
- Actions have three components: Goal, Feedback, Result
- Use feedback_callback for feedback messages
- Use get_result_async() for the final result
- Can check goal_handle.is_cancel_requested for cancellation
"""

import sys
import time
import rclpy
from rclpy.node import Node


# TODO: Implement CountdownServer class
# - Simulates counting down from a given number
# - Sends "feedback" via logging
# - Returns completion status
class CountdownServer(Node):
    def __init__(self):
        super().__init__('countdown_server')
        self.get_logger().info('Countdown server ready')

    def execute_countdown(self, target):
        """Execute countdown from target to 0"""
        # TODO: Implement countdown logic
        # - Loop from target down to 0
        # - Log each number as "feedback"
        # - Sleep 1 second between each number
        pass


# TODO: Implement CountdownClient class
# - Sends countdown goals
# - Handles feedback
# - Receives final result
class CountdownClient(Node):
    def __init__(self):
        super().__init__('countdown_client')

    def send_countdown_request(self, target):
        """Send countdown request"""
        # TODO: Implement request logic
        # - Call server's execute_countdown
        # - Receive and log feedback
        pass


def main():
    rclpy.init()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        node = CountdownServer()
        print("Starting Countdown Server...")
        print("Waiting for client requests")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        node = CountdownClient()
        print("Starting Countdown Client...")
        
        # Send countdown requests
        for target in [5, 10]:
            print(f"\n--- Counting down from {target} ---")
            node.send_countdown_request(target)
            print("Countdown complete!")
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
