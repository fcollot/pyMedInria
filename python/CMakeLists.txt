# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Configuration
################################################################################

set(cmake_args
    -D "PYNCPP_BUILD_EMBEDDABLE_PYTHON:BOOL=${MED_BUILD_PYTHON}"
    )

set(prefix "${CMAKE_CURRENT_BINARY_DIR}")

################################################################################
# External project
################################################################################

ExternalProject_Add(${PROJECT_NAME}_python
    PREFIX "${prefix}"
    DOWNLOAD_DIR "${prefix}/download"
    SOURCE_DIR "${prefix}/source"
    BINARY_DIR "${prefix}/build"
    STAMP_DIR "${prefix}/stamp"
    TMP_DIR "${prefix}/tmp"
    CMAKE_ARGS ${cmake_args}
    GIT_REPOSITORY "https://github.com/fcollot/pyncpp.git"
    GIT_TAG 1.0.x
    GIT_SHALLOW True
    GIT_PROGRESS True
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
        )
    "
    )

install(CODE "
    execute_process(COMMAND ${CMAKE_COMMAND}
        --install \"${prefix}/build\"
        --prefix \"\${CMAKE_INSTALL_PREFIX}\"
        --component Runtime
        )
    "
    EXCLUDE_FROM_ALL
    COMPONENT Runtime
    )
