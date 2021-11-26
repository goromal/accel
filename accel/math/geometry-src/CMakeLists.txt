cmake_minimum_required(VERSION 2.8.12)
project(python_utilities)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
find_package(Eigen3 REQUIRED)
add_subdirectory(lib/pybind11)
add_subdirectory(lib/utils)
include_directories(
  lib/utils/include
  ${EIGEN3_INCLUDE_DIRS}
)

pybind11_add_module(utils_logging src/utils_plugins/logging.cpp)
pybind11_add_module(utils_quat    src/utils_plugins/quat.cpp)
pybind11_add_module(utils_xform   src/utils_plugins/xform.cpp)
# pybind11_add_module(utils_support src/utils_plugins/support.cpp)
