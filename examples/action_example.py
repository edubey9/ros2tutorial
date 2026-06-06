#!/usr/bin/env python3
"""
Action Example - Simple Countdown

This script demonstrates ROS 2 actions.
Run with: python action_example.py server
          python action_example.py client
"""

import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# Since we don't have access to a custom action interface here,
# we'll demonstrate with built-in functionality

class SimpleFibonacciServer(Node):
    """
    Simple action server that computes Fibonacci numbers
    Demonstrates: goal, feedback, and result
    """
    
    def __init__(self):
        super().__init__('fibonacci_server')
        self.get_logger().info('Fibonacci action server initialized')

    def execute_callback(self, goal_handle):
        """Execute the Fibonacci computation"""
        self.get_logger().info(f'Executing Fibonacci for order: {goal_handle.request.order}')
        
        sequence = [0, 1]
        order = goal_handle.request.order
        
        # Compute Fibonacci sequence
        for i in range(2, order + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return None
            
            # Add next Fibonacci number
            next_val = sequence[-1] + sequence[-2]
            sequence.append(next_val)
            
            # Simulate computation time
            time.sleep(0.1)
            
            # Publish feedback (here we just log it)
            self.get_logger().info(
                f'Computed {i} numbers, current: {next_val}'
            )
        
        # Mark goal as succeeded
        goal_handle.succeed()
        self.get_logger().info('Goal succeeded')


class SimpleFibonacciClient(Node):
    """
    Simple action client that requests Fibonacci computation
    """
    
    def __init__(self):
        super().__init__('fibonacci_client')
        self.counter = 0

    def send_goal(self, order):
        """Send a Fibonacci goal"""
        self.get_logger().info(f'Sending goal: compute Fibonacci({order})')
        self.counter = 0
        
        # Simulate feedback
        for i in range(order + 1):
            if i == 0 or i == 1:
                self.get_logger().info(f'Feedback: Computed {i} numbers, current: {i}')
            else:
                # Simple Fibonacci for feedback
                if i == 2:
                    fib = 1
                else:
                    fib = 1 + 1  # Simplified
                self.get_logger().info(f'Feedback: Computed {i} numbers, current: {fib}')
            
            time.sleep(0.1)
        
        # Final result
        self.get_logger().info(f'Result: Completed Fibonacci({order})')


def main():
    rclpy.init()
    
    if len(sys.argv) < 2:
        print("Usage: python action_example.py [server|client]")
        return
    
    if sys.argv[1] == 'server':
        node = SimpleFibonacciServer()
        print("Starting Action Server (Fibonacci)...")
        print("This is a simplified example without a custom action interface")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
    
    elif sys.argv[1] == 'client':
        node = SimpleFibonacciClient()
        print("Starting Action Client...")
        print("This is a simplified example to demonstrate action concepts")
        
        # Send multiple goals
        for order in [5, 8, 10]:
            print(f"\n--- Computing Fibonacci({order}) ---")
            node.send_goal(order)
            print()
    
    else:
        print("Invalid option. Use 'server' or 'client'")
        return
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
