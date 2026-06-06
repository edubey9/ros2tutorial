#!/usr/bin/env python3
"""
Service Example

This script demonstrates ROS 2 services.
Run with: python service_example.py server
          python service_example.py client
"""

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import time


class AddTwoIntsServer(Node):
    """Simple service server that adds two integers"""
    
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Incoming request: a={request.a}, b={request.b}'
        )
        self.get_logger().info(f'Sending back response: {response.sum}')
        return response


class AddTwoIntsClient(Node):
    """Simple service client that calls the add service"""
    
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        self.get_logger().info(f'Sending request: {a} + {b}')
        future = self.cli.call_async(request)
        # Block until the response arrives (robust, no fixed timeout)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main():
    rclpy.init()
    
    if len(sys.argv) < 2:
        print("Usage: python service_example.py [server|client]")
        return
    
    if sys.argv[1] == 'server':
        node = AddTwoIntsServer()
        print("Starting Service Server...")
        print("Waiting for client requests...")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
        
    elif sys.argv[1] == 'client':
        node = AddTwoIntsClient()
        print("Starting Service Client...")
        
        # Make multiple requests
        requests = [(2, 3), (5, 7), (10, 20), (100, 50)]

        for a, b in requests:
            result = node.send_request(a, b)
            if result is not None:
                print(f"Result: {a} + {b} = {result.sum}")
            else:
                print(f"Service call failed for {a} + {b}")
            time.sleep(0.5)
    else:
        print("Invalid option. Use 'server' or 'client'")
        return
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
