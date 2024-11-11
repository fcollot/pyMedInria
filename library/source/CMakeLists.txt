# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

cmake_policy(SET CMP0074 NEW)

################################################################################
# Project
################################################################################

set(PYMED_VERSION "${PYMED_VERSION_MAJOR}.${PYMED_VERSION_MINOR}.${PYMED_VERSION_PATCH}")

project(pyMedInria_library VERSION "${PYMED_VERSION}")

################################################################################
# CMake modules
################################################################################

include(CMakePackageConfigHelpers)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/pyMedInria_commands.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/pyMedInria_commands.cmake
    @ONLY
    )

include(${CMAKE_CURRENT_BINARY_DIR}/pyMedInria_commands.cmake)

################################################################################
# Dependencies
################################################################################

find_package(pyncpp REQUIRED)

find_package(${PYMED_QT_PACKAGE} REQUIRED COMPONENTS Core)

################################################################################
# Files
################################################################################

set(headers
    pyMedInria.h
    pyMedInria/conversion.h
    pyMedInria/conversion/qobject.h
    pyMedInria/export.h
    )

set(sources
    pyMedInria.cpp
    pyMedInria/conversion/qobject.cpp
    )

################################################################################
# Library
################################################################################

set(target ${PROJECT_NAME})

pyMedInria_add_library(${target} SHARED
    ${headers}
    ${sources}
    )

################################################################################
# Target properties
################################################################################

if(UNIX)
    set(rpath ${CMAKE_INSTALL_RPATH})

    if(APPLE)
        set(rpath_prefix "@executable_path")
    else()
        set(rpath_prefix "\$ORIGIN")
    endif()

    if(APPLE)
        set(bin_dir "MacOS")
        set(lib_dir "Frameworks")
    else()
        set(bin_dir "${CMAKE_INSTALL_BINDIR}")
        set(lib_dir "${CMAKE_INSTALL_LIBDIR}")
    endif()

    file(RELATIVE_PATH relative_lib_dir "/${bin_dir}" "/${lib_dir}")
    list(APPEND rpath "${rpath_prefix}/${relative_lib_dir}")

    set_target_properties(${target} PROPERTIES
        INSTALL_RPATH "${rpath}"
        )
endif()

################################################################################
# Compile definitions
################################################################################

if(UNIX)
    if(APPLE)
        set(lib_dir "Frameworks")
    else()
        set(lib_dir "${CMAKE_INSTALL_LIBDIR}")
    endif()

endif()

target_compile_definitions(${target} PUBLIC
    PYTHON_HOME=".."
    PYTHON_LIB_DIR="${lib_dir}"
    PYMED_SHIBOKEN_PACKAGE="${PYMED_SHIBOKEN_PACKAGE}"
    PYMED_PYSIDE_PACKAGE="${PYMED_PYSIDE_PACKAGE}"
    )

################################################################################
# Includes
################################################################################

target_include_directories(${target}
    PRIVATE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/pyMedInria>"
    PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/pyMedInria>"
    )

################################################################################
# Link
################################################################################

target_link_libraries(${target} PUBLIC
    ${PYMED_QT_PACKAGE}::Core
    pyncpp_cpp_api
    )

################################################################################
# Config files
################################################################################

foreach(config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})

    configure_package_config_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/pyMedInriaConfig.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfig.cmake"
        INSTALL_PREFIX "/foo"
        INSTALL_DESTINATION "/foo/${PYMED_SHARE_SUBDIR}"
        )

    write_basic_package_version_file(
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfigVersion.cmake"
        VERSION ${PYMED_VERSION}
        COMPATIBILITY SameMinorVersion
        )

endforeach()

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/pyMedInria_update_dependencies.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/pyMedInria_update_dependencies.cmake
    @ONLY
    )

################################################################################
# Install/Export
################################################################################

install(TARGETS ${target}
    EXPORT ${target}_export

    RUNTIME
    DESTINATION "${CMAKE_INSTALL_BINDIR}"
    COMPONENT Runtime

    LIBRARY
    DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    COMPONENT Runtime

    ARCHIVE
    DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    COMPONENT Development
    )

install(EXPORT ${target}_export
    DESTINATION "${PYMED_SHARE_SUBDIR}"
    COMPONENT Development
    )

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/pyMedInria"
    COMPONENT Development
    FILES_MATCHING PATTERN "*.h"
    PATTERN "CMakeLists.txt" EXCLUDE
    )

foreach(config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})
    install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfigVersion.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/pyMedInria_commands.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/pyMedInria_update_dependencies.cmake"
        CONFIGURATIONS ${config}
        DESTINATION "${PYMED_SHARE_SUBDIR}"
        COMPONENT Development
        )
endforeach()

