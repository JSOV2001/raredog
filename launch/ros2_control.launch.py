# Libraries for file handling
import os
from ament_index_python import get_package_share_directory
import xacro
# Libraries for node launching
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

description_share_filepath = get_package_share_directory("raredog")

xacro_filepath = os.path.join(description_share_filepath, "description", "raredog.urdf.xacro")
robot_description_file = xacro.process_file(xacro_filepath)
controller_filepath = os.path.join(description_share_filepath, "config", "controllers.yaml")

use_sim_time = LaunchConfiguration("use_sim_time")
use_ros2_control = LaunchConfiguration('use_ros2_control')

def generate_launch_description():
    use_sim_time_declaration = DeclareLaunchArgument(
        "use_sim_time", 
        default_value= "true", 
        description= "Use sim time if true"
    )

    use_ros2_control_declaration = DeclareLaunchArgument(
        'use_ros2_control',
        default_value='true',
        description='Use ros2_control if true'
    )

    robot_state_publisher_node = Node(
        package= "robot_state_publisher",
        executable= "robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description_file.toxml(),
                "use_sim_time": use_sim_time
            }
        ]
    )
    
    gazebo_cmd = ExecuteProcess(
        cmd = ["gazebo", "-s", "libgazebo_ros_factory.so"]
    )
    
    gazebo_spawner_node = Node(
        package = "gazebo_ros",
        executable = "spawn_entity.py",
        arguments = [
            '-topic', 'robot_description', 
            '-entity', 'raredog',
            "-x", "0.0",
            "-y", "0.0",
            "-z", "0.25"
        ],
    )

    controller_manager_node = Node(
        package= "controller_manager",
        executable= "ros2_control_node",
        namespace= "raredog",
        remappings=[
            ("~/robot_description", "robot_description")
        ]
    )

    joint_state_broadcaster_spawner_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments= ["joint_state_broadcaster"],
    )
    
    joint_group_position_controller_spawner_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments= ["joint_group_position_controller"],
    )

    nodes_to_run = [
        use_sim_time_declaration,
        use_ros2_control_declaration,
        robot_state_publisher_node, 
        gazebo_cmd, 
        gazebo_spawner_node,
        controller_manager_node,
        joint_state_broadcaster_spawner_node,
        joint_group_position_controller_spawner_node
    ]
    return LaunchDescription(nodes_to_run)