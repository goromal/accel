include_directories(${PROJECT_SOURCE_DIR}/pyceres-src/pybind11/include)
include_directories(${PROJECT_SOURCE_DIR}/internal)

set(PYBIND11_CPP_STANDARD -std=c++11)
add_subdirectory(${PROJECT_SOURCE_DIR}/pyceres-src/pybind11)
pybind11_add_module(pyceres ${PROJECT_SOURCE_DIR}/pyceres-src/python_bindings/python_module.cpp
        ${PROJECT_SOURCE_DIR}/pyceres-src/python_bindings/ceres_examples_module.cpp
        ${PROJECT_SOURCE_DIR}/pyceres-src/python_bindings/custom_cpp_cost_functions.cpp)

target_link_libraries(pyceres INTERFACE manif-geom-cpp PRIVATE ceres)

message(STATUS "Python Bindings for Ceres (pyceres) have been added")
