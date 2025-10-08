from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    camera_node = Node(
        package='hikcamera',
        executable='hikcamera_node',
        name='mvs_camera_node',
        output='screen',
        parameters=[
            '/home/zngyim/Desktop/XJTU-RMV-Task04/src/hikcamera/config/hik_params.yaml'
        ]
    )

    rviz = ExecuteProcess(
        cmd=['rviz2', '-d', '/home/zngyim/Desktop/XJTU-RMV-Task04/src/hikcamera/config/hikcamera.rviz'],
        output='screen'
    )

    # 当相机节点退出时，自动关闭 RViz
    exit_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=camera_node,
            on_exit=[rviz]
        )
    )

    return LaunchDescription([camera_node, rviz, exit_handler])
