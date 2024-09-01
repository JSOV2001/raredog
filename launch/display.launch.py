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
rviz_config_filepath = os.path.join(description_share_filepath, "config", "display.rviz")

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

    rviz_cmd = ExecuteProcess(
        cmd= ["rviz2", "-d", rviz_config_filepath]
    )

    joint_state_publisher_gui_node = Node(
        package= "joint_state_publisher_gui",
        executable= "joint_state_publisher_gui",
    )

    nodes_to_run = [
        use_sim_time_declaration,
        use_ros2_control_declaration,
        robot_state_publisher_node, 
        rviz_cmd, 
        joint_state_publisher_gui_node
    ]
    return LaunchDescription(nodes_to_run)
       
