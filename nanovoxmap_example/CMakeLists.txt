cmake_minimum_required(VERSION 3.22)
project(nanovoxmap_example)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

set(dependencies 
  "rclcpp"
  "geometry_msgs"
  "nav_msgs"
  "tf2"
  "tf2_ros"
)


# Add the ground-truth node for RViz.
add_executable(camera_lidar_ground_truth_node
  src/main.cpp
  src/SubscribeAndPublish.cpp)
target_include_directories(camera_lidar_ground_truth_node PRIVATE include)
ament_target_dependencies(camera_lidar_ground_truth_node ${dependencies})
install(TARGETS camera_lidar_ground_truth_node DESTINATION lib/${PROJECT_NAME} )

install(DIRECTORY
  launch 
  config
  urdf
  meshes
  worlds
  DESTINATION share/${PROJECT_NAME}/
)

install(FILES LICENSE DESTINATION share/${PROJECT_NAME})


ament_package()
