cmake_minimum_required(VERSION 3.11)

project(cpp-rime)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(APPLE)
    # set(CMAKE_C_COMPILER "/home/cc/soft/gcc-13/bin/gcc")
    # set(CMAKE_CXX_COMPILER "/home/cc/soft/gcc-13/bin/g++")
    # set(CMAKE_C_COMPILER "/usr/local/bin/gcc-8")
    # set(CMAKE_CXX_COMPILER "/usr/local/bin/g++-8")
endif()

# 添加模块目录
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# 基本设置
include(CompilerSettings)

# 下载安装依赖库
# 用3rdparty/nlohmann替换，更加简单
# include(ProjectJsonCpp)

# 添加子目录
add_subdirectory("./src")
add_subdirectory("./app")
