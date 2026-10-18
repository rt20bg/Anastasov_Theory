cmake_minimum_required(VERSION 3.10)
project(evm_engine C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -Wall -Wextra)
endif()

find_package(OpenMP QUIET)

add_executable(evm_engine
    src/main.c
    src/engine.c
    src/forcefield.c
    src/xyz_io.c
)

if(NOT MSVC)
    target_link_libraries(evm_engine PRIVATE m)
endif()

if(OpenMP_C_FOUND)
    target_link_libraries(evm_engine PRIVATE OpenMP::OpenMP_C)
    message(STATUS "OpenMP found -- building with multi-threaded force computation")
else()
    message(STATUS "OpenMP not found -- building single-threaded (still correct, just slower)")
endif()
