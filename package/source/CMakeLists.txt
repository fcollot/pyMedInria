# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

################################################################################
# Project
################################################################################

set(MED_VERSION "${MED_VERSION_MAJOR}.${MED_VERSION_MINOR}.${MED_VERSION_PATCH}")

project(pyMedInria_package VERSION "${MED_VERSION}")

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

if(UNIX OR MED_SYMLINK_SOURCE_PACKAGE)
    install(CODE "
        file(REMOVE_RECURSE \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}/pymedinria\")
        file(CREATE_LINK
            \"${CMAKE_CURRENT_SOURCE_DIR}/pymedinria\"
            \"\${CMAKE_INSTALL_PREFIX}/${package_subdir}/pymedinria\"
            SYMBOLIC
            )
        "
        )

    set(exclude_from_all EXCLUDE_FROM_ALL)
else()
    set(exclude_from_all)
endif()

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/pymedinria"
    DESTINATION "${package_subdir}"
    ${exclude_from_all}
    COMPONENT Runtime
    PATTERN "*.pyc" EXCLUDE
    PATTERN "__pycache__" EXCLUDE
    )

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    DESTINATION "${package_subdir}"
    COMPONENT Runtime
    )
