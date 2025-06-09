from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    launch_dir = PathJoinSubstitution([FindPackageShare('mavros_control'), 'launch'])
    spinnaker_dir = PathJoinSubstitution([FindPackageShare('spinnaker_camera_driver'), 'launch'])
    return LaunchDescription([
        IncludeLaunchDescription(
            PathJoinSubstitution([launch_dir, 'base.launch.py'])
        ),
        IncludeLaunchDescription(
            PathJoinSubstitution([spinnaker_dir, 'driver_node.launch.py']),
            launch_arguments={"camera_name": "color_camera", "serial":"'25101138'"}.items()
        ),
        IncludeLaunchDescription(
            PathJoinSubstitution([spinnaker_dir, 'driver_node.launch.py']),
            launch_arguments={"camera_name": "mono_camera", "serial":"'25132946'"}.items()
        ),
    ])

