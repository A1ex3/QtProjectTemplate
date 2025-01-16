cmake_minimum_required(VERSION 3.25)

project(QtProjectTemplate)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(QT_DIR "$ENV{QT_FULL_DIRECTORY}/lib/cmake/Qt6")

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(QtProjectTemplate WIN32
    src/main.cpp
)

target_link_libraries(QtProjectTemplate PRIVATE Qt6::Widgets)
