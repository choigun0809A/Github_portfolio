cmake_minimum_required(VERSION 3.10)

project(r)

set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "$ENV{HOME}/libs/libtorch")


find_package(Torch REQUIRED)

set(CMAKE_CXX_STANDARD 17)


add_executable(r main.cpp model.h)
target_link_libraries(r PUBLIC "${TORCH_LIBRARIES}")

