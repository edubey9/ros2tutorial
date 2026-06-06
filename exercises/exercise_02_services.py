#!/usr/bin/env python3
"""
Exercise 2: Services

Challenge: Create a service that multiplies two numbers.

Instructions:
1. Create a Service Server node
   - Service name: 'multiply_numbers'
   - Request: two integers (a, b)
   - Response: their product (result)
   - Note: We'll use AddTwoInts service interface, but multiply instead of add

2. Create a Service Client node
   - Call the multiply service with different pairs
   - Example: (3, 4) should return 12
   - Log the results

3. Run server in one terminal, client in another

Hints:
- Use create_service(AddTwoInts, 'multiply_numbers', callback)
- Use create_client(AddTwoInts, 'multiply_numbers')
- Wait for service with wait_for_service()
- Use call_async() to call the service
- Use rclpy.spin_until_future_complete(self, future) to wait for the response
"""

import sys
import time
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


# TODO: Implement MultiplyServer class
# - Constructor should create a service
# - Callback should multiply the two numbers
class MultiplyServer(Node):
    def __init__(self):
        super().__init__('multiply_server')
        # TODO: Create service
        pass

    def multiply_callback(self, request, response):
        # TODO: Implement multiplication logic
        # Set response.sum to the product of request.a and request.b
        pass


# TODO: Implement MultiplyClient class
# - Constructor should create a client and wait for service
# - Should be able to send multiply requests
class MultiplyClient(Node):
    def __init__(self):
        super().__init__('multiply_client')
        # TODO: Create client
        # TODO: Wait for service
        pass

    def send_request(self, a, b):
        # TODO: Create and send request
        # TODO: Wait for response and log result
        pass


def main():
    rclpy.init()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        node = MultiplyServer()
        print("Running Service Server...")
        print("Ready to multiply numbers")
        print("Press Ctrl+C to stop")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        node = MultiplyClient()
        print("Running Service Client...")
        
        # Test cases
        test_cases = [(3, 4), (5, 6), (10, 10), (7, 8)]
        
        for a, b in test_cases:
            print(f"\nMultiplying {a} * {b}...")
            node.send_request(a, b)
            # TODO: Handle response
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
