#!/usr/bin/env python3
"""
Publisher/Subscriber Example

This script can run as either a publisher or subscriber.
Run with: python pub_sub_example.py publisher
          python pub_sub_example.py subscriber
"""

import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random


class Talker(Node):
    """Simple publisher that sends greetings"""
    
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2! Message #{self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


class Listener(Node):
    """Simple subscriber that receives messages"""
    
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main():
    rclpy.init()
    
    if len(sys.argv) < 2:
        print("Usage: python pub_sub_example.py [publisher|subscriber]")
        return
    
    if sys.argv[1] == 'publisher':
        node = Talker()
        print("Starting Publisher (Talker)...")
        print("Press Ctrl+C to stop")
    elif sys.argv[1] == 'subscriber':
        node = Listener()
        print("Starting Subscriber (Listener)...")
        print("Press Ctrl+C to stop")
    else:
        print("Invalid option. Use 'publisher' or 'subscriber'")
        return
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
