# 链接pthread库
find_package(Threads REQUIRED)

# # find_library(jsoncpp NAMES "../3rdparty/jsoncpp")
# set(JSON_CPP_DIR "../3rdparty/jsoncpp")
# set(JSON_CPP_INCLUDE_DIR ${JSON_CPP_DIR}/include/json)
# find_library(JSON_CPP jsoncpp ${JSON_CPP_DIR}/lib NO_DEFAULT_PATH)
add_library(processor processor.cc utils.cc)

target_include_directories(processor
    PUBLIC
    ../include
    ../3rdparty
    # ${JSONCPP_INCLUDE_DIR}
)

# target_link_libraries(processor PRIVATE Threads::Threads ${JSON_CPP})
target_link_libraries(processor
    PRIVATE
    Threads::Threads
    # JsonCpp
)
