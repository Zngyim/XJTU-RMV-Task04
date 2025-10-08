cmake_minimum_required(VERSION 3.8)
project(hikcamera)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

# Include directories
set(MVS_SDK_PATH ./../../)
include_directories(${MVS_SDK_PATH}/include)
link_directories(${MVS_SDK_PATH}/lib)

# Create executable
add_executable(hikcamera_node src/main.cpp)
target_link_libraries(hikcamera_node
  MvCameraControl
  MediaProcess
  ${OpenCV_LIBS}
)
ament_target_dependencies(hikcamera_node
  rclcpp
  std_msgs
  sensor_msgs
  cv_bridge
)

# Install
install(TARGETS
  hikcamera_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package() 

