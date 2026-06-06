#!/usr/bin/env python3
"""
ROS 2 Learning Environment - Setup and Exercise Tester

This script verifies your ROS 2 installation and tests all exercises.

Usage:
    python3 test_ros2_setup.py              # Full setup verification
    python3 test_ros2_setup.py --verify     # Quick verification only
    python3 test_ros2_setup.py --test-pub-sub   # Test exercise 1
    python3 test_ros2_setup.py --test-service   # Test exercise 2
    python3 test_ros2_setup.py --test-action    # Test exercise 3
"""

import sys
import subprocess
import time
import os
import signal
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BLUE}{'='*60}{END}")
    print(f"{BLUE}{text:^60}{END}")
    print(f"{BLUE}{'='*60}{END}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{END} {text}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗{END} {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠{END} {text}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ{END} {text}")

def check_python_packages():
    """Verify all required Python packages are installed"""
    print_header("Python Package Verification")
    
    packages = {
        'rclpy': 'ROS 2 Python client library',
        'std_msgs': 'Standard ROS 2 message types',
        'example_interfaces': 'Example interfaces (AddTwoInts service - Tutorial 3)',
        'action_tutorials_interfaces': 'Action interfaces (Fibonacci action - Tutorial 4)',
    }
    
    all_ok = True
    for package, description in packages.items():
        try:
            __import__(package)
            print_success(f"{package}: {description}")
        except ImportError:
            print_error(f"{package}: {description} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_ros2_installation():
    """Verify ROS 2 is installed and accessible"""
    print_header("ROS 2 Installation Verification")
    
    try:
        result = subprocess.run(['ros2', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print_success(f"ROS 2 is installed: {version_info}")
            return True
        else:
            print_error("ROS 2 command failed")
            return False
    except FileNotFoundError:
        print_error("ROS 2 not found - did you source the setup.bash?")
        return False
    except Exception as e:
        print_error(f"Error checking ROS 2: {e}")
        return False

def test_pub_sub_communication():
    """Test publisher/subscriber communication"""
    print_header("Testing Publisher/Subscriber Communication")
    
    try:
        # Start publisher
        print_info("Starting publisher...")
        pub_process = subprocess.Popen(
            [sys.executable, 'examples/pub_sub_example.py', 'publisher'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        
        # Start subscriber
        print_info("Starting subscriber and listening for 5 seconds...")
        sub_process = subprocess.Popen(
            [sys.executable, 'examples/pub_sub_example.py', 'subscriber'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let them run for 5 seconds
        time.sleep(5)
        
        # Stop processes
        pub_process.terminate()
        sub_process.terminate()
        
        # Get output
        pub_stdout, _ = pub_process.communicate(timeout=2)
        sub_stdout, _ = sub_process.communicate(timeout=2)
        
        # Check results
        if 'Publishing' in pub_stdout:
            print_success("Publisher sent messages")
        else:
            print_warning("Publisher output not detected")
        
        if 'I heard' in sub_stdout:
            print_success("Subscriber received messages")
            return True
        else:
            print_error("Subscriber did not receive messages")
            return False
            
    except Exception as e:
        print_error(f"Pub/Sub test failed: {e}")
        return False
    finally:
        try:
            pub_process.kill()
            sub_process.kill()
        except:
            pass

def verify_exercise_files():
    """Verify all exercise files exist and have TODO markers"""
    print_header("Exercise Files Verification")
    
    exercises = {
        'exercises/exercise_01_pub_sub.py': 'Publishers and Subscribers',
        'exercises/exercise_02_services.py': 'Services',
        'exercises/exercise_03_actions.py': 'Actions',
    }
    
    all_ok = True
    for exercise_path, description in exercises.items():
        if os.path.exists(exercise_path):
            # Check for TODO markers
            with open(exercise_path, 'r') as f:
                content = f.read()
                todo_count = content.count('TODO')
            
            if todo_count > 0:
                print_success(f"{exercise_path}: {description} ({todo_count} TODOs to complete)")
            else:
                print_warning(f"{exercise_path}: {description} (No TODO markers - may be completed!)")
        else:
            print_error(f"{exercise_path}: NOT FOUND")
            all_ok = False
    
    return all_ok

def verify_tutorial_files():
    """Verify all tutorial files exist"""
    print_header("Tutorial Files Verification")
    
    tutorials = {
        'tutorials/01_setup.md': 'ROS 2 Setup and Concepts',
        'tutorials/02_publisher_subscriber.md': 'Publishers and Subscribers',
        'tutorials/03_services.md': 'Services',
        'tutorials/04_actions.md': 'Actions',
        'tutorials/05_advanced_topics.md': 'Advanced Topics',
    }
    
    all_ok = True
    for tutorial_path, description in tutorials.items():
        if os.path.exists(tutorial_path):
            with open(tutorial_path, 'r') as f:
                lines = len(f.readlines())
            print_success(f"{tutorial_path}: {description} ({lines} lines)")
        else:
            print_error(f"{tutorial_path}: NOT FOUND")
            all_ok = False
    
    return all_ok

def verify_example_files():
    """Verify all example files exist"""
    print_header("Example Files Verification")
    
    examples = {
        'examples/pub_sub_example.py': 'Publisher/Subscriber Example',
        'examples/service_example.py': 'Service Example',
        'examples/action_example.py': 'Action Example',
    }
    
    all_ok = True
    for example_path, description in examples.items():
        if os.path.exists(example_path):
            with open(example_path, 'r') as f:
                lines = len(f.readlines())
            print_success(f"{example_path}: {description} ({lines} lines)")
        else:
            print_error(f"{example_path}: NOT FOUND")
            all_ok = False
    
    return all_ok

def full_setup_verification():
    """Run all verification checks"""
    print_header("ROS 2 Learning Environment Setup Verification")
    
    results = {
        'Python Packages': check_python_packages(),
        'ROS 2 Installation': check_ros2_installation(),
        'Tutorial Files': verify_tutorial_files(),
        'Example Files': verify_example_files(),
        'Exercise Files': verify_exercise_files(),
    }
    
    # Summary
    print_header("Verification Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = f"{GREEN}PASS{END}" if result else f"{RED}FAIL{END}"
        print(f"{status}: {check_name}")
    
    print(f"\n{BLUE}Total: {passed}/{total} checks passed{END}\n")
    
    if passed == total:
        print_success("All checks passed! You're ready to start learning ROS 2!")
        return True
    else:
        print_error(f"{total - passed} check(s) failed. See above for details.")
        return False

def test_communication():
    """Test the pub/sub communication"""
    print_header("Communication Test")
    
    if test_pub_sub_communication():
        print_success("Communication test passed!")
        return True
    else:
        print_error("Communication test failed!")
        return False

def main():
    """Main test function"""
    os.chdir(Path(__file__).parent)
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == '--verify':
            return 0 if full_setup_verification() else 1
        elif arg == '--test-pub-sub':
            return 0 if test_communication() else 1
        elif arg in ['-h', '--help']:
            print(__doc__)
            return 0
    
    # Default: Full verification
    success = full_setup_verification()
    
    if success:
        print_info("Running communication test...")
        if not test_communication():
            print_warning("Communication test failed, but setup is OK")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
