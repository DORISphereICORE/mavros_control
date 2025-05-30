import os
from launch import LaunchDescription
from launch_ros.actions import PushRosNamespace
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import GroupAction, IncludeLaunchDescription
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


def get_var(var, default):
    try:
        return os.environ[var]
    except:
        return default

def generate_launch_description():
    namespace = ''
    foxglove = True if get_var('FOXGLOVE', 'True')=='True' else False

    nodes = []

    # MAVROS
    mavros = GroupAction(
                    actions=[
                        # push_ros_namespace to set namespace of included nodes
                        PushRosNamespace(namespace),
                        # MAVROS
                        IncludeLaunchDescription(
                            XMLLaunchDescriptionSource([
                                PathJoinSubstitution([
                                    FindPackageShare('mavros_control'),
                                    'launch',
                                    'mavros.launch'
                                ])
                            ]),
                            launch_arguments={
                                "fcu_url": "tcp://0.0.0.0:5777@"
                            }.items()
                        ),
                    ]
                )
    nodes.append(mavros) 

    # Foxglove (web-based rviz)
    if foxglove:
        foxglove = GroupAction(
                        actions=[
                            # push_ros_namespace to set namespace of included nodes
                            PushRosNamespace(namespace),
                            # Foxglove
                            IncludeLaunchDescription(
                                XMLLaunchDescriptionSource([
                                    PathJoinSubstitution([
                                        FindPackageShare('foxglove_bridge'),
                                        'launch',
                                        'foxglove_bridge_launch.xml'
                                    ])
                                ]),
                            )
                        ]
                    )
        nodes.append(foxglove)

    return LaunchDescription(nodes)