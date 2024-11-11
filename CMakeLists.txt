# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION 3.19)

################################################################################
# Version
################################################################################

find_package(Git)
set(_success FALSE)

if(GIT_EXECUTABLE)
    execute_process(COMMAND ${GIT_EXECUTABLE} describe --tags --always
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        OUTPUT_VARIABLE _git_describe
        )

    if (_git_describe MATCHES "^v([0-9]+)\\.([0-9]+)(-([0-9]+))?.*$")
        set(PYMED_VERSION_MAJOR ${CMAKE_MATCH_1})
        set(PYMED_VERSION_MINOR ${CMAKE_MATCH_2})
        if(CMAKE_MATCH_4)
            set(PYMED_VERSION_PATCH ${CMAKE_MATCH_4})
        else()
            set(PYMED_VERSION_PATCH 0)
        endif()
        set(_success TRUE)
    endif()
endif()

if(_success)
    message(STATUS "pyMedInria version number generated from git: ${PYMED_VERSION_MAJOR}.${PYMED_VERSION_MINOR}.${PYMED_VERSION_PATCH}")
else()
    set(PYMED_VERSION_MAJOR 0)
    set(PYMED_VERSION_MINOR 0)
    set(PYMED_VERSION_PATCH 0)
    message(WARNING "Cannot use git to generate a version number for pyMedInria. Defaulting to 0.0.0")
endif()

################################################################################
# Project
################################################################################

set(PYMED_VERSION "${PYMED_VERSION_MAJOR}.${PYMED_VERSION_MINOR}.${PYMED_VERSION_PATCH}")

project(pyMedInria VERSION "${PYMED_VERSION}")

################################################################################
# CMake modules
################################################################################

include(CMakeDependentOption)
include(CTest)
include(ExternalProject)

################################################################################
# Settings
################################################################################

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

get_property(GENERATOR_IS_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)

if(NOT GENERATOR_IS_MULTI_CONFIG AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(FETCHCONTENT_BASE_DIR "${CMAKE_BINARY_DIR}")

set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

option(PYMED_BUILD_STANDALONE "Build the standalone" ON)

cmake_dependent_option(PYMED_BUILD_LIBRARY "Build the library (a wrapper over pyncpp with helper bindings for Qt, ITK and VTK)" ON "NOT PYMED_BUILD_STANDALONE" ON)

cmake_dependent_option(PYMED_BUILD_PYTHON "Build a custom Python interpreter" OFF "NOT PYMED_BUILD_STANDALONE" ON)

if(WIN32)
    string(CONCAT symlink_message
        "Use a symbolic link to the Python package in the source tree, so that"
        " modifications to the source code directly affect the package installed"
        " in the build tree (permissions to create symbolic links are necessary)."
        )
    option(PYMED_SYMLINK_SOURCE_PACKAGE ${symlink_message} OFF)
else()
    option(PYMED_USE_QT5 "Use Qt5 instead of Qt6" OFF)
endif()

if(PYMED_USE_QT5)
    set(PYMED_QT_PACKAGE "Qt5")
    set(PYMED_PYSIDE_PACKAGE "PySide2")
    set(PYMED_SHIBOKEN_PACKAGE "shiboken2")
else()
    set(PYMED_QT_PACKAGE "Qt6")
    set(PYMED_PYSIDE_PACKAGE "PySide6")
    set(PYMED_SHIBOKEN_PACKAGE "shiboken6")
endif()

################################################################################
# Paths
################################################################################

set(PYMED_ROOT_BASE "${CMAKE_CURRENT_BINARY_DIR}")
set(PYMED_ROOT "${PYMED_ROOT_BASE}/$<CONFIG>")

if(WIN32)
    set(CMAKE_INSTALL_BINDIR "bin")
    set(CMAKE_INSTALL_LIBDIR "bin")
    set(CMAKE_INSTALL_INCLUDEDIR "include")
    set(share_subdir "cmake")
else()
    include(GNUInstallDirs)
    set(share_subdir "share/cmake/pyMedInria")
endif()

set(PYMED_SHARE_SUBDIR "${share_subdir}" CACHE PATH "")

################################################################################
# Subdirectories
################################################################################

add_subdirectory(pyMedInria)

add_subdirectory(python)

if(PYMED_BUILD_LIBRARY)
    add_subdirectory(library)
endif()

if(PYMED_BUILD_STANDALONE)
    add_subdirectory(standalone)
endif()
