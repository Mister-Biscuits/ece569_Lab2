from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("ur3e_on_table"), "urdf", "ur3e_on_table.urdf.xacro"]
            ),
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    rviz_config = PathJoinSubstitution(
        [FindPackageShare("ur3e_on_table"), "rviz", "ur3e_on_table_default.rviz"]
    )

    # Publishes /joint_states, so no joint_state_publisher_gui here
    pick_and_place_node = Node(
        package="ur3e_on_table",
        executable="pick_and_place",
        output="screen",
    )
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
        arguments=["-d", rviz_config],
    )

    return LaunchDescription(
        [
            pick_and_place_node,
            robot_state_publisher_node,
            rviz_node,
        ]
    )