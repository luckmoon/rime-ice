# 添加根目录到头文件搜索目录
# include_directories(BEFORE ${PROJECT_SOURCE_DIR})

# 设置可执行文件输出路径
# set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)

# # 设置编译器选项
# if (CMAKE_CXX_COMPILER_ID MATCHES "GNU")
#     # 各个编译模式下共用的编译选项
#     set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -pthread")

#     # 各编译模式专有的编译选项
#     set(CMAKE_CXX_FLAGS_DEBUG          "-Og -g")
#     set(CMAKE_CXX_FLAGS_MINSIZEREL     "-Os -DNDEBUG")
#     set(CMAKE_CXX_FLAGS_RELEASE        "-O3 -DNDEBUG")
#     set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g")
# else()
#     message(FATAL "Your compiler is not supported.")
# endif()