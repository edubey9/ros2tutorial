# ROS 2 Learning Progress Tracker

Use this file to track your progress through the ROS 2 learning curriculum. Check off each item as you complete it!

## Setup Phase

### Installation and Configuration
- [ ] ROS 2 Humble installed on your system
- [ ] Python 3.10+ installed
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Can run `ros2 --version` without errors
- [ ] Test script runs successfully (`python3 test_ros2_setup.py` or `bash test_setup.sh`)
- [ ] All project files are present and readable

### First Run
- [ ] Run publisher example in one terminal
- [ ] Run subscriber example in another terminal
- [ ] Saw messages flowing from publisher to subscriber
- [ ] Understand the difference between publisher and subscriber

---

## Tutorial 1: Setup and Concepts (01_setup.md)

**Time Estimate: 30 minutes**

### Reading and Understanding
- [ ] Read the "What is ROS 2?" section
- [ ] Understand nodes, topics, services, and actions concepts
- [ ] Know the difference between pub/sub and services
- [ ] Can explain node lifecycle (init, spin, shutdown)

### Knowledge Verification
- [ ] Can explain what a node is
- [ ] Can name the three communication patterns in ROS 2
- [ ] Understand why pub/sub is asynchronous
- [ ] Know what a ROS 2 message is

### Practical
- [ ] Ran the minimal node example
- [ ] Used `ros2 node list` command
- [ ] Used `ros2 topic list` command

---

## Tutorial 2: Publishers and Subscribers (02_publisher_subscriber.md)

**Time Estimate: 1-2 hours**

### Reading and Understanding
- [ ] Read publisher and subscriber sections
- [ ] Understand QoS (Quality of Service) parameter
- [ ] Know what a message type is
- [ ] Understand timer callbacks
- [ ] Understand message callbacks

### Knowledge Verification
- [ ] Can explain how to create a publisher
- [ ] Can explain how to create a subscriber
- [ ] Know what the `10` in `create_publisher(..., 10)` means
- [ ] Understand how messages flow asynchronously
- [ ] Can name 3 message types

### Practical
- [ ] Ran `pub_sub_example.py publisher` and `pub_sub_example.py subscriber`
- [ ] Saw messages flowing between them
- [ ] Used `ros2 topic echo /chatter` to monitor messages
- [ ] Modified the example to publish different data

### Exercise 1: Publisher/Subscriber Counter
- [ ] Read exercise_01_pub_sub.py completely
- [ ] Understand all TODO comments
- [ ] Implemented PublisherNode class
- [ ] Implemented SubscriberNode class
- [ ] Tested publisher runs without errors
- [ ] Tested subscriber connects to publisher
- [ ] Verified messages are being received correctly
- [ ] Did NOT move to next tutorial until this works

### Verification
- [ ] `ros2 topic echo /counter` shows messages
- [ ] Publisher shows "Publishing" messages
- [ ] Subscriber shows "Received" messages
- [ ] Exercise runs for at least 10 seconds without errors

---

## Tutorial 3: Services (03_services.md)

**Time Estimate: 1-2 hours**

### Reading and Understanding
- [ ] Read service concepts section
- [ ] Understand request-response pattern
- [ ] Know the difference between services and pub/sub
- [ ] Understand service servers and clients
- [ ] Know how to wait for a service

### Knowledge Verification
- [ ] Can explain how services differ from pub/sub
- [ ] Understand why services are synchronous
- [ ] Know when to use a service instead of pub/sub
- [ ] Can name the AddTwoInts service type
- [ ] Understand request and response structures

### Practical
- [ ] Ran `service_example.py server` and `service_example.py client`
- [ ] Saw correct results returned from service
- [ ] Used `ros2 service list` command
- [ ] Used `ros2 service call` from command line
- [ ] Modified example to use different numbers

### Exercise 2: Multiplication Service
- [ ] Read exercise_02_services.py completely
- [ ] Understand all TODO comments
- [ ] Implemented MultiplyServer class
- [ ] Implemented MultiplyClient class
- [ ] Tested server starts and waits for requests
- [ ] Tested client connects and sends requests
- [ ] Verified multiplication is calculated correctly
- [ ] Did NOT move to next tutorial until this works

### Verification
- [ ] `ros2 service list` shows /multiply_numbers
- [ ] `ros2 service call /multiply_numbers example_interfaces/srv/AddTwoInts "{a: 5, b: 6}"` returns correct result
- [ ] Server shows incoming requests
- [ ] Client shows returned results
- [ ] Exercise runs multiple requests successfully

---

## Tutorial 4: Actions (04_actions.md)

**Time Estimate: 1.5-2 hours**

### Reading and Understanding
- [ ] Read actions concepts section
- [ ] Understand goals, feedback, and results
- [ ] Know the difference between actions and services
- [ ] Understand when to use actions
- [ ] Know action server and client structure

### Knowledge Verification
- [ ] Can explain goals, feedback, and results
- [ ] Understand why actions are for long-running tasks
- [ ] Know when to use actions instead of services
- [ ] Understand asynchronous action execution
- [ ] Can name use cases for actions

### Practical
- [ ] Ran `action_example.py server` and `action_example.py client`
- [ ] Saw feedback messages during execution
- [ ] Received final results
- [ ] Understand the action flow

### Exercise 3: Countdown Action
- [ ] Read exercise_03_actions.py completely
- [ ] Understand all TODO comments
- [ ] Implemented CountdownServer class
- [ ] Implemented CountdownClient class
- [ ] Tested server starts successfully
- [ ] Tested client sends goals
- [ ] Verified feedback is being sent
- [ ] Did NOT move to next tutorial until this works

### Verification
- [ ] Server logs show countdown numbers
- [ ] Client receives feedback messages
- [ ] Final countdown complete message appears
- [ ] Can observe progress updates during execution

---

## Tutorial 5: Advanced Topics (05_advanced_topics.md)

**Time Estimate: 2-3 hours**

### Reading and Understanding
- [ ] Read parameters section
- [ ] Read launch files section
- [ ] Read debugging tools section
- [ ] Understand lifecycle nodes (optional)
- [ ] Understand rosbags for recording (optional)

### Knowledge Verification
- [ ] Can explain what parameters are
- [ ] Know how to pass parameters to a node
- [ ] Understand launch files
- [ ] Can name 3 ROS 2 debugging tools
- [ ] Know when to use rosbags

### Practical
- [ ] Used `ros2 param list` and `ros2 param get` commands
- [ ] Set parameters with `ros2 param set`
- [ ] Ran `rqt_graph` to see node relationships (if available)
- [ ] Used `ros2 node info` to inspect nodes
- [ ] Experimented with debugging commands

### Optional Advanced Topics
- [ ] Read lifecycle nodes section
- [ ] Understand state transitions
- [ ] Read rosbag section
- [ ] Tried recording and playing back data
- [ ] Explored Docker integration

---

## Completion Checklist

### All Tutorials Completed
- [ ] Tutorial 1: Setup ✓
- [ ] Tutorial 2: Publishers/Subscribers ✓
- [ ] Tutorial 3: Services ✓
- [ ] Tutorial 4: Actions ✓
- [ ] Tutorial 5: Advanced Topics ✓

### All Exercises Completed and Working
- [ ] Exercise 1: Publisher/Subscriber Counter ✓
- [ ] Exercise 2: Multiplication Service ✓
- [ ] Exercise 3: Countdown Action ✓

### Test Suite
- [ ] `python3 test_ros2_setup.py` passes all checks
- [ ] `bash test_setup.sh` passes all checks (bash version)
- [ ] Can run all examples without errors
- [ ] Can run all exercises without errors

### Self-Assessment
Rate your understanding on a scale of 1-5 (1=beginner, 5=expert):

- [ ] ROS 2 concepts: _____
- [ ] Publishers/Subscribers: _____
- [ ] Services: _____
- [ ] Actions: _____
- [ ] ROS 2 tools and debugging: _____
- [ ] Overall confidence: _____

### Knowledge Check

Answer these questions to verify your learning:

1. **What are the main communication patterns in ROS 2?**
   - [ ] Pub/Sub, Services, Actions

2. **When would you use a service instead of pub/sub?**
   - [ ] When you need synchronous request-response

3. **What's the main difference between services and actions?**
   - [ ] Actions have feedback and can be cancelled

4. **How do you start multiple nodes at once?**
   - [ ] Using launch files

5. **What command shows all running nodes?**
   - [ ] `ros2 node list`

---

## Next Steps After Completing This Course

### Recommended Learning Path

1. **Build Your First ROS 2 Package**
   - Create a new package with `ros2 pkg create`
   - Implement multiple nodes that communicate
   - Use parameters and launch files

2. **Explore the ROS 2 Ecosystem**
   - Navigation stack (Nav2)
   - Manipulation (MoveIt2)
   - Perception (perception_pcl)
   - Simulation (Gazebo)

3. **Join the Community**
   - Ask questions on ROS Discourse
   - Contribute to open source ROS 2 projects
   - Follow ROS 2 blog and tutorials

4. **Advanced Topics** (when ready)
   - Custom message types
   - Plugins and lifecycle nodes
   - Security and encryption
   - Real-time programming

### Resources to Explore

- [ ] ROS 2 GitHub organization
- [ ] Official ROS 2 tutorials
- [ ] Community projects on GitHub
- [ ] ROS 2 Discord community
- [ ] Local ROS meetup groups

---

## Notes and Personal Reflections

Use this space to write down:
- Concepts you found challenging
- Questions you want to explore further
- Ideas for projects using ROS 2
- Your learning progress observations

```
[Write your notes here]




```

---

## Summary

**Estimated Total Time: 6-10 hours**

This learning path covers all fundamental ROS 2 concepts. Once you complete this, you'll be ready to:
- Build custom ROS 2 nodes
- Design multi-node systems
- Use ROS 2 tools effectively
- Understand and work with existing ROS 2 packages

Good luck on your ROS 2 journey! 🚀
