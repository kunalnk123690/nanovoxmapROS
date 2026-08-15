# NanoVoxMap ROS 2 wrapper

This package wraps [NanoVoxMap](https://github.com/kunalnk123690/nanovoxmap) as a ROS 2 node. It synchronizes a `sensor_msgs/PointCloud2` stream with `nav_msgs/Odometry`, builds an occupancy map, and publishes occupied voxels and an optional ESDF point cloud.

## Build

Install ROS 2 and the package dependencies, then clone recursively into a ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone --recurse-submodules https://github.com/kunalnk123690/nanovoxmapROS.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

If the repository was cloned without submodules, run:

```bash
git submodule update --init --recursive
```

## Run

Edit `nanovoxmap_ros/config/mapping.yaml` for your point-cloud, odometry, output, and frame names, then run:

```bash
ros2 run nanovoxmap_ros nanovoxmap_ros_node --ros-args \
  --params-file "$(ros2 pkg prefix nanovoxmap_ros)/share/nanovoxmap_ros/config/mapping.yaml"
```
or include the node in your launch file
```
nanovoxmap_node = Node(
    package='nanovoxmap_ros',
    executable='nanovoxmap_ros_node',
    name='nanovoxmap_node',
    output='screen',
    parameters=[os.path.join(get_package_share_directory('nanovoxmap_ros'), 'config', 'mapping.yaml')]
)
```

The odometry pose must describe the point-cloud sensor in the configured world frame. See the YAML file for optional downsampling, ray clearing, occupancy, and ESDF settings.

## Example

The separate `nanovoxmap_example` package includes a Jackal Gazebo simulation. After building and sourcing the workspace, run:

```bash
ros2 launch nanovoxmap_example run_simulation.launch.py
```

## License

BSD 3-Clause. See [LICENSE](LICENSE).
