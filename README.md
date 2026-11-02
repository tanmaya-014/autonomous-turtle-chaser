# Autonomous Turtle Chaser — ROS 2 Humble

A multi-node ROS 2 system built in Python using the turtlesim simulator.

## Overview

The system allows a user to manually control the primary turtle (`turtle1`) using keyboard input, while a second turtle (`turtle2`) autonomously tracks and follows it in real time.

## Technologies

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- turtlesim
- rclpy
- geometry_msgs

## How it works

The `turtle_chaser` node:

1. Subscribes to `/turtle1/pose` to receive the target turtle's position.
2. Subscribes to `/turtle2/pose` to receive its own position and orientation.
3. Calculates the distance and desired heading towards the target.
4. Computes linear and angular velocity commands.
5. Publishes `geometry_msgs/Twist` messages to `/turtle2/cmd_vel`.

The controller runs periodically at 10 Hz.

## Run the project

Source ROS 2 and the workspace:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
source install/setup.bash
