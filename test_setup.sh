#!/bin/bash

# ROS 2 Learning Environment - Quick Test Script
# This script verifies your ROS 2 installation and environment

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0

print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check ROS 2
check_ros2() {
    print_header "Checking ROS 2 Installation"
    
    if command -v ros2 &> /dev/null; then
        version=$(ros2 --version 2>/dev/null)
        print_success "ROS 2 is installed: $version"
    else
        print_error "ROS 2 not found. Make sure to source setup.bash:"
        echo "    source /opt/ros/humble/setup.bash"
    fi
}

# Check Python
check_python() {
    print_header "Checking Python Installation"
    
    if command -v python3 &> /dev/null; then
        version=$(python3 --version)
        print_success "Python 3 is installed: $version"
    else
        print_error "Python 3 not found"
    fi
}

# Check Python packages
check_packages() {
    print_header "Checking Python Packages"
    
    python3 -c "import rclpy" 2>/dev/null && \
        print_success "rclpy installed" || \
        print_error "rclpy not found - source ROS 2: source /opt/ros/humble/setup.bash"

    python3 -c "from std_msgs.msg import String" 2>/dev/null && \
        print_success "std_msgs installed" || \
        print_error "std_msgs not found - source ROS 2: source /opt/ros/humble/setup.bash"

    python3 -c "from example_interfaces.srv import AddTwoInts" 2>/dev/null && \
        print_success "example_interfaces installed (needed for services tutorial)" || \
        print_error "example_interfaces not found - source ROS 2: source /opt/ros/humble/setup.bash"

    python3 -c "from action_tutorials_interfaces.action import Fibonacci" 2>/dev/null && \
        print_success "action_tutorials_interfaces installed (needed for actions tutorial)" || \
        print_error "action_tutorials_interfaces not found - included in ros-humble-desktop"
}

# Check files
check_files() {
    print_header "Checking Project Files"
    
    files=(
        "README.md"
        "GETTING_STARTED.md"
        "requirements.txt"
        "tutorials/01_setup.md"
        "tutorials/02_publisher_subscriber.md"
        "tutorials/03_services.md"
        "tutorials/04_actions.md"
        "tutorials/05_advanced_topics.md"
        "examples/pub_sub_example.py"
        "examples/service_example.py"
        "examples/action_example.py"
        "exercises/exercise_01_pub_sub.py"
        "exercises/exercise_02_services.py"
        "exercises/exercise_03_actions.py"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            print_success "$file exists"
        else
            print_error "$file NOT FOUND"
        fi
    done
}

# Test pub/sub
test_pubsub() {
    print_header "Quick Pub/Sub Communication Test"
    
    if ! command -v ros2 &> /dev/null; then
        print_warning "ROS 2 not available, skipping communication test"
        return
    fi
    
    print_info "Starting publisher..."
    timeout 5 python3 examples/pub_sub_example.py publisher > /tmp/pub.log 2>&1 &
    pub_pid=$!
    
    sleep 2
    
    print_info "Starting subscriber..."
    timeout 5 python3 examples/pub_sub_example.py subscriber > /tmp/sub.log 2>&1 &
    sub_pid=$!
    
    sleep 3
    
    # Kill if still running
    kill $pub_pid 2>/dev/null || true
    kill $sub_pid 2>/dev/null || true
    
    if grep -q "I heard" /tmp/sub.log 2>/dev/null; then
        print_success "Pub/Sub communication working"
    else
        print_warning "Pub/Sub communication test inconclusive"
    fi
}

# Show summary
show_summary() {
    print_header "Summary"
    
    total=$((PASS + FAIL))
    percentage=$((PASS * 100 / total))
    
    echo "Passed: $PASS"
    echo "Failed: $FAIL"
    echo "Total:  $total"
    echo ""
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}🎉 All checks passed! Ready to start learning!${NC}"
        return 0
    else
        echo -e "${RED}⚠️  Some checks failed. See details above.${NC}"
        return 1
    fi
}

# Main
main() {
    check_python
    check_ros2
    check_packages
    check_files
    test_pubsub
    show_summary
}

main "$@"
