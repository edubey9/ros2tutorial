#!/usr/bin/env python3
"""
Action Example - Fibonacci

This script demonstrates ROS 2 actions with a REAL action server and client
that communicate over the ROS graph (run them in two separate terminals).

It uses the Fibonacci action from action_tutorials_interfaces, which is
included in the ROS 2 Humble desktop installation (and the
osrf/ros:humble-desktop Docker image).

The Fibonacci action is defined as:
    # Goal
    int32 order
    ---
    # Result
    int32[] sequence
    ---
    # Feedback
    int32[] partial_sequence

Run with: python action_example.py server
          python action_example.py client
"""

import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient, CancelResponse
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    """
    Action server that computes a Fibonacci sequence.
    Demonstrates: receiving a goal, publishing feedback, returning a result,
    and handling cancellation.
    """

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback,
        )
        self.get_logger().info('Fibonacci action server ready')

    def cancel_callback(self, goal_handle):
        """Accept all cancel requests"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute the Fibonacci computation, publishing feedback as we go"""
        self.get_logger().info(f'Executing goal: Fibonacci({goal_handle.request.order})')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Compute the next Fibonacci number
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            )

            # Publish feedback to the client
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {list(feedback_msg.partial_sequence)}')

            # Simulate a long-running computation
            time.sleep(0.5)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f'Goal succeeded with result: {list(result.sequence)}')
        return result


class FibonacciActionClient(Node):
    """
    Action client that sends a goal, prints feedback as it arrives,
    and prints the final result.
    """

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        """Send a Fibonacci goal and register callbacks"""
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal: compute Fibonacci({order})')
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Called when the server accepts or rejects the goal"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Called every time the server publishes feedback"""
        partial = list(feedback_msg.feedback.partial_sequence)
        self.get_logger().info(f'Feedback: {partial}')

    def get_result_callback(self, future):
        """Called when the final result arrives"""
        result = future.result().result
        self.get_logger().info(f'Result: {list(result.sequence)}')
        # Stop spinning once we have the result
        rclpy.shutdown()


def main():
    rclpy.init()

    if len(sys.argv) < 2:
        print("Usage: python action_example.py [server|client]")
        return

    if sys.argv[1] == 'server':
        node = FibonacciActionServer()
        print("Starting Action Server (Fibonacci)...")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
        node.destroy_node()
        rclpy.shutdown()

    elif sys.argv[1] == 'client':
        node = FibonacciActionClient()
        print("Starting Action Client...")
        node.send_goal(10)
        try:
            # Spin until get_result_callback calls rclpy.shutdown()
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")

    else:
        print("Invalid option. Use 'server' or 'client'")
        rclpy.shutdown()


if __name__ == '__main__':
    main()
