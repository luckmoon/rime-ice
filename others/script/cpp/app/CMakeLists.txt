# find_package(OpenMP REQUIRED)
add_executable(main main.cc)
add_executable(main2 main2.cc)

target_link_libraries(main processor)
target_link_libraries(main2 processor)
