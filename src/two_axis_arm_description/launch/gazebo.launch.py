import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_name = 'two_axis_arm_description'

    xacro_file = PathJoinSubstitution([
        FindPackageShare(package_name),
        'urdf',
        'two_axis_arm_gazebo.urdf.xacro'
    ])

    robot_description_content = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file
        ]),
        value_type=str
    )

    robot_description = {
        'robot_description': robot_description_content,
        'use_sim_time': True
    }

    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    spawn_robot_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'two_axis_arm',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0'
        ],
        output='screen'
    )

    delayed_spawn_robot_node = TimerAction(
        period=5.0,
        actions=[spawn_robot_node]
    )

    return LaunchDescription([
        gazebo_node,
        robot_state_publisher_node,
        delayed_spawn_robot_node
    ])
