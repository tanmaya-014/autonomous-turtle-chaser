from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    turtlesim = Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen'
    )

    spawn = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/spawn',
            'turtlesim/srv/Spawn',
            "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
        ],
        output='screen'
    )

    chaser = Node(
        package='autonomous_turtle_chaser',
        executable='turtle_chaser',
        output='screen'
    )

    return LaunchDescription([
        turtlesim,
        TimerAction(period=2.0, actions=[spawn]),
        TimerAction(period=4.0, actions=[chaser])
    ])
