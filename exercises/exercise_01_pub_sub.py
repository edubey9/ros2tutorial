#!/usr/bin/env python3
"""
Exercise 1: Publishers and Subscribers

Challenge: Create a publisher that sends numbers 0-10 over a topic,
           and a subscriber that receives and logs them.

Instructions:
1. Create a Publisher node that publishes integers from 0 to 10
   - Use std_msgs.msg.Int32 for the message type
   - Publish one number per second
   - Topic name: 'counter'

2. Create a Subscriber node that receives these numbers
   - Subscribe to the 'counter' topic
   - Log each received number with a message like: "Received: 5"

3. Run both nodes simultaneously in different terminals

Hints:
- Use create_publisher(Int32, 'counter', 10)
- Use create_subscription(Int32, 'counter', callback, 10)
- Use self.create_timer() for periodic publishing
- To stop after publishing 10, call self.timer.cancel() in the timer callback
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


# TODO: Implement PublisherNode class
# - Constructor should create a publisher and timer
# - Timer callback should publish numbers 0-10
class PublisherNode(Node):
    def __init__(self):
        super().__init__('counter_publisher')
        # TODO: Create publisher
        # TODO: Create timer with 1 second period
        pass

    def timer_callback(self):
        # TODO: Implement publishing logic
        pass


# TODO: Implement SubscriberNode class
# - Constructor should create a subscription
# - Callback should log received numbers
class SubscriberNode(Node):
    def __init__(self):
        super().__init__('counter_subscriber')
        # TODO: Create subscription
        pass

    def listener_callback(self, msg):
        # TODO: Implement logging logic
        pass


def main():
    rclpy.init()
    
    # Choose which node to run
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'pub':
        node = PublisherNode()
        print("Running Publisher...")
    else:
        node = SubscriberNode()
        print("Running Subscriber...")
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
