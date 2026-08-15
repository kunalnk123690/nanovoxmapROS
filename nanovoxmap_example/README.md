# NanoVoxMap example

ROS 2 Jazzy and Gazebo example using a simulated Jackal with LiDAR and depth sensors.

## Dependencies

- ROS 2 Jazzy with `colcon` and `rosdep`
- Gazebo and ROS integration: `ros_gz_sim`, `ros_gz_bridge`
- `robot_state_publisher`, `xacro`, `rviz2`
- `interactive_marker_twist_server`

Install package dependencies from the repository root:

```bash
rosdep install --from-paths . --ignore-src -r -y
```

## Build and run

```bash
git submodule update --init --recursive
colcon build --symlink-install
source install/setup.bash
ros2 launch nanovoxmap_example run_simulation.launch.py
```

Licensed under the [BSD 3-Clause License](LICENSE).
