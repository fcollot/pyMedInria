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
    -D "PYMED_VERSION_MAJOR:STRING=${PYMED_VERSION_MAJOR}"
    -D "PYMED_VERSION_MINOR:STRING=${PYMED_VERSION_MINOR}"
    -D "PYMED_VERSION_PATCH:STRING=${PYMED_VERSION_PATCH}"
    -D "PYMED_QT_PACKAGE:PATH=${PYMED_QT_PACKAGE}"
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
    DEPENDS ${PROJECT_NAME} ${PROJECT_NAME}_library
    CMAKE_ARGS ${cmake_args}
    INSTALL_COMMAND ${CMAKE_COMMAND}
    --install "<BINARY_DIR>"
    --prefix "${PYMED_ROOT}"
    --config $<CONFIG>
    )

################################################################################
# Tests
################################################################################

if(APPLE)
    set(executable "pyMedInria.app/Contents/MacOS/pyMedInria")
else()
    set(executable "pyMedInria${CMAKE_EXECUTABLE_SUFFIX}")
endif()

add_test(NAME ${PROJECT_NAME}_test_no_gui
    COMMAND "${PYMED_ROOT}/${CMAKE_INSTALL_BINDIR}/${executable}" --test no-gui
    )

add_test(NAME ${PROJECT_NAME}_test_gui
    COMMAND "${PYMED_ROOT}/${CMAKE_INSTALL_BINDIR}/${executable}" --test gui
    )

set_property(TEST ${PROJECT_NAME}_test_no_gui PROPERTY LABELS TEST_NO_GUI)
set_property(TEST ${PROJECT_NAME}_test_gui PROPERTY LABELS TEST_GUI)

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

################################################################################
# Packaging
################################################################################

add_subdirectory(packaging)
