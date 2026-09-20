from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # mode picks the joint state source: gui (sliders), test, or lissajous
    mode = LaunchConfiguration("mode")
    mode_arg = DeclareLaunchArgument(
        "mode",
        default_value="test",
        description="Joint state source: gui, test, or lissajous",
    )

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

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        condition=IfCondition(PythonExpression(["'", mode, "' == 'gui'"])),
    )
    test_node = Node(
        package="ur3e_on_table",
        executable="test",
        output="screen",
        condition=IfCondition(PythonExpression(["'", mode, "' == 'test'"])),
    )
    lissajous_node = Node(
        package="ur3e_on_table",
        executable="lissajous",
        output="screen",
        condition=IfCondition(PythonExpression(["'", mode, "' == 'lissajous'"])),
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
            mode_arg,
            joint_state_publisher_node,
            test_node,
            lissajous_node,
            robot_state_publisher_node,
            rviz_node,
        ]
    )