# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Configuration
################################################################################

set(cmake_args
    -D "CMAKE_MINIMUM_REQUIRED_VERSION:STRING=${CMAKE_MINIMUM_REQUIRED_VERSION}"
    -D "CMAKE_BUILD_TYPE:PATH=${CMAKE_BUILD_TYPE}"
    -D "CMAKE_CXX_STANDARD:STRING=${CMAKE_CXX_STANDARD}"
    -D "CMAKE_CXX_STANDARD_REQUIRED:BOOL=${CMAKE_CXX_STANDARD_REQUIRED}"
    -D "CMAKE_MAKE_PROGRAM:PATH=${CMAKE_MAKE_PROGRAM}"
    -D "CMAKE_PREFIX_PATH:PATH=${MED_ROOT}"
    -D "MED_VERSION_MAJOR:STRING=${MED_VERSION_MAJOR}"
    -D "MED_VERSION_MINOR:STRING=${MED_VERSION_MINOR}"
    -D "MED_VERSION_PATCH:STRING=${MED_VERSION_PATCH}"
    -D "MED_QT_PACKAGE:PATH=${MED_QT_PACKAGE}"
    -D "MED_PYSIDE_PACKAGE:PATH=${MED_PYSIDE_PACKAGE}"
    )

set(prefix "${CMAKE_CURRENT_BINARY_DIR}")

################################################################################
# External project
################################################################################

ExternalProject_Add(${PROJECT_NAME}_standalone
    PREFIX "${prefix}"
    DOWNLOAD_DIR "${prefix}/download"
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/source"
    BINARY_DIR "${prefix}/build"
    STAMP_DIR "${prefix}/stamp"
    TMP_DIR "${prefix}/tmp"
    DEPENDS ${PROJECT_NAME}_library
    CMAKE_ARGS ${cmake_args}
    INSTALL_COMMAND ${CMAKE_COMMAND}
    --install "<BINARY_DIR>"
    --prefix "${MED_ROOT}"
    )

################################################################################
# Install
################################################################################

install(CODE "
    execute_process(COMMAND ${CMAKE_COMMAND}
        --install \"${prefix}/build\"
        --prefix \"\${CMAKE_INSTALL_PREFIX}\"
        --config $<CONFIG>
        )
    "
    )

install(CODE "
    execute_process(COMMAND ${CMAKE_COMMAND}
        --install \"${prefix}/build\"
        --prefix \"\${CMAKE_INSTALL_PREFIX}\"
        --config $<CONFIG>
        --component Runtime
        )
    "
    EXCLUDE_FROM_ALL
    COMPONENT Runtime
    )
