import math

import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class TurtleChaser(Node):

    def __init__(self):
        super().__init__('turtle_chaser')

        # Store the latest positions of both turtles
        self.target_pose = None
        self.chaser_pose = None

        # Subscribe to the primary turtle's position
        self.target_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.target_callback,
            10
        )

        # Subscribe to the chaser turtle's position
        self.chaser_sub = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self.chaser_callback,
            10
        )

        # Publish movement commands for turtle2
        self.cmd_pub = self.create_publisher(
            Twist,
            '/turtle2/cmd_vel',
            10
        )

        # Run the control algorithm 10 times per second
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Turtle chaser node started!')

    def target_callback(self, msg):
        self.target_pose = msg

    def chaser_callback(self, msg):
        self.chaser_pose = msg

    def control_loop(self):

        # Wait until we have received both turtles' positions
        if self.target_pose is None or self.chaser_pose is None:
            return

        # Calculate the distance and direction to the target
        dx = self.target_pose.x - self.chaser_pose.x
        dy = self.target_pose.y - self.chaser_pose.y

        distance = math.sqrt(dx**2 + dy**2)

        desired_theta = math.atan2(dy, dx)

        # Calculate angular error
        error = desired_theta - self.chaser_pose.theta

        # Keep angular error between -pi and +pi
        error = math.atan2(math.sin(error), math.cos(error))

        # Create a velocity message
        msg = Twist()

        # Turn towards the target
        msg.angular.z = max(-2.0, min(2.0, 4.0 * error))

        # Move forward only when reasonably aligned
        if abs(error) < 0.5 and distance > 0.25:
            msg.linear.x = min(2.0, 1.5 * distance)
        else:
            msg.linear.x = 0.0

        # Stop when close enough
        if distance <= 0.25:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        # Send the velocity command
        self.cmd_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleChaser()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Send a stop command before shutting down
        stop_msg = Twist()
        node.cmd_pub.publish(stop_msg)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
