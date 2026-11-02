# Autonomous Turtle Chaser 

A multi-node ROS 2 system built using python and turtlesim.

## Overview

The system allows a user to manually control the primary turtle (turtle1) using keyboard input, while a second turtle (turtle2) autonomously tracks and follows it in real time.

## Technologies

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- turtlesim
- rclpy
- geometry_msgs

## How it works

The turtle_chaser node:

1. Subscribes to topic - /turtle1/pose to receive the target turtle's position.
2. Subscribes to topic - /turtle2/pose to receive chaser turtle's position and orientation.
3. Calculates distance between current and target positions, calculates angular error - or simply difference between desired heading and current heading.
4. Computes linear and angular velocity Twist commands for chaser turtle, through simple proportional control mechansim. (Greater the error, greater the correction)
5. Publishes geometry_msgs/Twist messages to topic - /turtle2/cmd_vel

The controller runs through a defined control loop, which executes every 0.1 seconds.

## Run the project

Source ROS 2 and the workspace:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
source install/setup.bash
