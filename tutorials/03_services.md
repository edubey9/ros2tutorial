# Tutorial 3: Services

Services provide a synchronous request-response communication pattern. A client sends a request to a server, waits for a response, and then continues. This is different from Publishers/Subscribers which are asynchronous.

## Use Cases for Services

- **Parameter queries**: Get configuration values
- **One-time computations**: Calculate inverse kinematics, plan a path
- **State changes**: Trigger actions with immediate feedback
- **Database queries**: Fetch data and wait for results

## Service Definition

A service consists of a request and a response. ROS 2 provides built-in service types, but you can also create custom ones.

### Common Built-in Services

```python
# Two integers, return one integer (from example_interfaces,
# which ships with ROS 2 — note: std_srvs does NOT contain AddTwoInts)
from example_interfaces.srv import AddTwoInts

# The request has:
# int64 a
# int64 b
# The response has:
# int64 sum
```

## Service Server

A Service Server waits for requests and sends responses.

### Simple Service Server Example

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        # Create a service server
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        # request.a and request.b contain the client's request
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending back response: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    minimal_service.get_logger().info('Service ready to accept requests')
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Service Client

A Service Client sends requests and waits for responses.

### Simple Service Client Example

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import time

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        # Create a service client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

    def send_request(self, a, b):
        # Create a request
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        # Send the request asynchronously
        self.future = self.cli.call_async(request)
        # Wait for the response
        rclpy.spin_until_future_complete(self, self.future)
        
        if self.future.result() is not None:
            self.get_logger().info(f'Result: {self.future.result().sum}')
        else:
            self.get_logger().error('Service call failed')

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    
    # Send multiple requests
    minimal_client.send_request(2, 3)
    minimal_client.send_request(5, 7)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running Service Server and Client

Terminal 1 (Service Server):
```bash
source /opt/ros/humble/setup.bash
python3 service_server.py
```

Terminal 2 (Service Client):
```bash
source /opt/ros/humble/setup.bash
python3 service_client.py
```

Terminal 3 (Optional - Test via CLI):
```bash
source /opt/ros/humble/setup.bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
```

## Practical Example: Calculator Service

### Service Server (Calculator)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class CalculatorService(Node):
    def __init__(self):
        super().__init__('calculator_service')
        self.srv = self.create_service(
            AddTwoInts,
            'calculator/add',
            self.add_callback
        )
        # Could add more services for subtract, multiply, etc.

    def add_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Add request: {request.a} + {request.b} = {response.sum}'
        )
        return response

def main(args=None):
    rclpy.init(args=args)
    calculator = CalculatorService()
    calculator.get_logger().info('Calculator service ready')
    rclpy.spin(calculator)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client (User)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class CalculatorClient(Node):
    def __init__(self):
        super().__init__('calculator_client')
        self.cli = self.create_client(AddTwoInts, 'calculator/add')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for calculator service...')

    def perform_calculation(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        self.future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result().sum

def main(args=None):
    rclpy.init(args=args)
    client = CalculatorClient()
    
    # Perform calculations
    result = client.perform_calculation(10, 20)
    print(f"10 + 20 = {result}")
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Service vs Publisher/Subscriber

| Feature | Service | Pub/Sub |
|---------|---------|---------|
| Communication | Request-Response | One-way (Async) |
| Blocking | Client waits for response | Non-blocking |
| Use Case | One-time queries | Continuous data streams |
| Complexity | Simple interface | Can handle fast data rates |
| Latency | Synchronous | Lower latency |

## Key Takeaways

1. **Services are synchronous** - clients wait for responses
2. **Services are good for** queries and one-time operations
3. **Multiple clients** can call the same service
4. **Naming convention** for services is `/service_namespace/service_name`
5. **Error handling** is important - always check if the service call succeeded

## Next Steps

Now that you understand services, move on to **Tutorial 4: Actions** to learn about asynchronous, long-running tasks with feedback.
