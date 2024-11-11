# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

################################################################################
# Project
################################################################################

set(PYMED_VERSION "${PYMED_VERSION_MAJOR}.${PYMED_VERSION_MINOR}.${PYMED_VERSION_PATCH}")

project(pyMedInria_package VERSION "${PYMED_VERSION}")

################################################################################
# Dependencies
################################################################################

find_package(pyncpp REQUIRED)

################################################################################
# Python package
################################################################################

file(GLOB_RECURSE sources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.py"
    )

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in"
    "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    @ONLY)

################################################################################
# Install
################################################################################

set(package_subdir "${CMAKE_INSTALL_LIBDIR}/pyMedInria")

install(CODE "
    if(NOT EXISTS \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}\")
        file(MAKE_DIRECTORY \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}\")
    endif()
    "
    COMPONENT Runtime
    )

if(UNIX OR PYMED_SYMLINK_SOURCE_PACKAGE)
    install(CODE "
        file(REMOVE_RECURSE \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}/pymedinria\")
        file(CREATE_LINK
            \"${CMAKE_CURRENT_SOURCE_DIR}/pymedinria\"
            \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}/pymedinria\"
            SYMBOLIC
            )
        "
        )

    install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/pymedinria"
        DESTINATION "${package_subdir}"
        EXCLUDE_FROM_ALL
        COMPONENT Runtime
        PATTERN "*.pyc" EXCLUDE
        PATTERN "__pycache__" EXCLUDE
        )
else()
    install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/pymedinria"
        DESTINATION "${package_subdir}"
        COMPONENT Runtime
        PATTERN "*.pyc" EXCLUDE
        PATTERN "__pycache__" EXCLUDE
        )
endif()

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    DESTINATION "${package_subdir}"
    COMPONENT Runtime
    )
