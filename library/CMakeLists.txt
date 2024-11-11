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
    -D "CMAKE_PREFIX_PATH:PATH=${PYMED_ROOT}"
    -D "CMAKE_INSTALL_BINDIR:PATH=${CMAKE_INSTALL_BINDIR}"
    -D "CMAKE_INSTALL_LIBDIR:PATH=${CMAKE_INSTALL_LIBDIR}"
    -D "CMAKE_INSTALL_INCLUDEDIR:PATH=${CMAKE_INSTALL_INCLUDEDIR}"
    -D "PYMED_SHARE_SUBDIR:PATH=${PYMED_SHARE_SUBDIR}"
    -D "PYMED_VERSION_MAJOR:STRING=${PYMED_VERSION_MAJOR}"
    -D "PYMED_VERSION_MINOR:STRING=${PYMED_VERSION_MINOR}"
    -D "PYMED_VERSION_PATCH:STRING=${PYMED_VERSION_PATCH}"
    -D "PYMED_QT_PACKAGE:PATH=${PYMED_QT_PACKAGE}"
    -D "PYMED_PYSIDE_PACKAGE:STRING=${PYMED_PYSIDE_PACKAGE}"
    -D "PYMED_SHIBOKEN_PACKAGE:PATH=${PYMED_SHIBOKEN_PACKAGE}"
    )

set(prefix "${CMAKE_CURRENT_BINARY_DIR}")

################################################################################
# External project
################################################################################

ExternalProject_Add(${PROJECT_NAME}_library
    PREFIX "${prefix}"
    DOWNLOAD_DIR "${prefix}/download"
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/source"
    BINARY_DIR "${prefix}/build"
    STAMP_DIR "${prefix}/stamp"
    TMP_DIR "${prefix}/tmp"
    DEPENDS ${PROJECT_NAME}_python
    CMAKE_ARGS ${cmake_args}
    INSTALL_COMMAND ${CMAKE_COMMAND}
    --install "<BINARY_DIR>"
    --prefix "${PYMED_ROOT}"
    --config $<CONFIG>
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

foreach(component Runtime Development)
    install(CODE "
        execute_process(COMMAND ${CMAKE_COMMAND}
            --install \"${prefix}/build\"
            --prefix \"\${CMAKE_INSTALL_PREFIX}\"
            --config $<CONFIG>
            --component ${component}
            )
        "
        EXCLUDE_FROM_ALL
        COMPONENT ${component}
        )
endforeach()
