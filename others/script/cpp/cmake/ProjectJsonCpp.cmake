# 导入插件
include(ExternalProject)
include(GNUInstallDirs)

# 下载安装依赖库
ExternalProject_Add(jsoncpp
    # 项目根目录
    PREFIX ${CMAKE_SOURCE_DIR}/deps/jsoncpp
    # 下载名
    DOWNLOAD_NAME jsoncpp-1.9.5.tar.gz
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    # 下载链接（支持多源下载）
    URL https://github.com/open-source-parsers/jsoncpp/archive/refs/tags/1.9.5.tar.gz
    # sha256哈希值校验
    URL_HASH SHA256=f409856e5920c18d0c2fb85276e24ee607d2a09b5e7d5f0a371368903c275da2
    # cmake命令
    CMAKE_COMMAND ${CMAKE_COMMAND}
    # cmake参数
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
               -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
               -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
               -DJSONCPP_WITH_TESTS=OFF
               -DJSONCPP_WITH_PKGCONFIG_SUPPORT=OFF
               -DBUILD_STATIC_LIBS=ON
    # 日志记录
    LOG_CONFIGURE 1
    LOG_BUILD 1
    LOG_INSTALL 1
)

# jsoncpp的库路径和头文件目录
ExternalProject_Get_Property(jsoncpp INSTALL_DIR)
set(JSONCPP_INCLUDE_DIR ${INSTALL_DIR}/include)
set(JSONCPP_LIBRARY ${INSTALL_DIR}/${CMAKE_INSTALL_LIBDIR}/${CMAKE_STATIC_LIBRARY_PREFIX}jsoncpp${CMAKE_STATIC_LIBRARY_SUFFIX})
file(MAKE_DIRECTORY ${JSONCPP_INCLUDE_DIR})  # Must exist.

# JsonCpp库
add_library(JsonCpp STATIC IMPORTED GLOBAL)
set_property(TARGET JsonCpp PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${JSONCPP_INCLUDE_DIR})
set_property(TARGET JsonCpp PROPERTY IMPORTED_LOCATION ${JSONCPP_LIBRARY})
add_dependencies(JsonCpp jsoncpp)

# 取消临时定义
unset(INSTALL_DIR)