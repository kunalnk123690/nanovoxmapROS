import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]),
        ' ',
        PathJoinSubstitution([
            FindPackageShare('nanovoxmap_example'),
            'urdf',
            'jackal.urdf.xacro',
        ]),
    ])
    robot_description = {'robot_description': robot_description_content}

    example_share = get_package_share_directory('nanovoxmap_example')
    default_world = os.path.join(example_share, 'worlds', 'warehouse.world')
    world = LaunchConfiguration('world')
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load',
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py',
        )),
        launch_arguments={
            'gz_args': ['-v 4 -r --headless-rendering ', world],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'jackal',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5',
            '-R', '0.0',
            '-P', '0.0',
            '-Y', '0.0',
        ],
        output='screen',
    )

    ground_truth_node = Node(
        package='nanovoxmap_example',
        executable='camera_lidar_ground_truth_node',
        output='screen',
    )

    sensor_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/jackal/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/jackal/ground_truth@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
            '/jackal/IMU@sensor_msgs/msg/Imu@gz.msgs.IMU',
            '/jackal/velodyne@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/jackal/velodyne/points@sensor_msgs/msg/PointCloud2@'
            'gz.msgs.PointCloudPacked',
            '/jackal/realsense/image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/jackal/realsense/camera_info@sensor_msgs/msg/CameraInfo@'
            'gz.msgs.CameraInfo',
            '/jackal/realsense/depth_image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/jackal/realsense/points@sensor_msgs/msg/PointCloud2@'
            'gz.msgs.PointCloudPacked',
            '/jackal/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/jackal/camera/camera_info@sensor_msgs/msg/CameraInfo@'
            'gz.msgs.CameraInfo',
        ],
        output='screen',
    )

    interactive_marker_node = Node(
        package='interactive_marker_twist_server',
        executable='marker_server',
        name='twist_marker_server',
        output='screen',
        parameters=[{'link_name': 'base_link', 'robot_name': 'jackal'}],
        remappings=[('cmd_vel', '/jackal/cmd_vel')],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    nanovoxmap_node = Node(
        package='nanovoxmap_ros',
        executable='nanovoxmap_ros_node',
        name='nanovoxmap_node',
        output='screen',
        parameters=[os.path.join(
            get_package_share_directory('nanovoxmap_ros'),
            'config',
            'mapping.yaml',
        )],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(example_share, 'config', 'jackal_visual.rviz')],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    return LaunchDescription([
        world_arg,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        sensor_bridge,
        ground_truth_node,
        interactive_marker_node,
        rviz,
        TimerAction(period=5.0, actions=[nanovoxmap_node]),
    ])
