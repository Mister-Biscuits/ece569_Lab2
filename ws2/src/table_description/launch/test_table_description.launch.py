from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    xacro_path = PathJoinSubstitution(
        [FindPackageShare("table_description"), "urdf", "table.urdf.xacro"]
    )
    rviz_path = PathJoinSubstitution(
        [FindPackageShare("table_description"), "rviz", "table_default.rviz"]
    )

    # Get URDF via xacro
    robot_description_content = Command(
        [PathJoinSubstitution([FindExecutable(name="xacro")]), " ", xacro_path]
    )
    robot_description = {"robot_description": robot_description_content}

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="both",
        arguments=["-d", rviz_path],
    )

    return LaunchDescription([robot_state_publisher_node, rviz_node])
