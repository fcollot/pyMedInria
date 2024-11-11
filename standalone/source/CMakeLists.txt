# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

################################################################################
# Project
################################################################################

set(PYMED_VERSION "${PYMED_VERSION_MAJOR}.${PYMED_VERSION_MINOR}.${PYMED_VERSION_PATCH}")

project(pyMedInria_standalone VERSION "${PYMED_VERSION}")

################################################################################
# Dependencies
################################################################################

find_package(pyMedInria REQUIRED)

find_package(${PYMED_QT_PACKAGE} REQUIRED COMPONENTS Core Widgets)

################################################################################
# Files
################################################################################

set(sources
    main.cpp
    )

################################################################################
# Executable
################################################################################

set(target ${PROJECT_NAME})

pyMedInria_add_executable(${target} WIN32
    ${sources}
    )

################################################################################
# Target properties
################################################################################

set(properties OUTPUT_NAME pyMedInria)

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

    list(APPEND properties INSTALL_RPATH "${rpath}")

    if(APPLE)
        list(APPEND properties MACOSX_BUNDLE TRUE)
    endif()
endif()

set_target_properties(${target} PROPERTIES ${properties})

################################################################################
# Link
################################################################################

target_link_libraries(${target} PUBLIC
    pyMedInria_library
    ${PYMED_QT_PACKAGE}::Core
    ${PYMED_QT_PACKAGE}::Widgets
    )

################################################################################
# Install/Export
################################################################################

install(TARGETS ${target}
    RUNTIME
    DESTINATION "${CMAKE_INSTALL_BINDIR}"
    COMPONENT Runtime

    BUNDLE
    DESTINATION "${CMAKE_INSTALL_BINDIR}"
    COMPONENT Runtime
    )

install(CODE "
    execute_process(
        COMMAND \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/python${CMAKE_EXECUTABLE_SUFFIX}\" -m ensurepip
        )
    "
    COMPONENT Runtime
    )

install(CODE "
    execute_process(
        COMMAND \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/python${CMAKE_EXECUTABLE_SUFFIX}\"
        -m pip install -e \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/pyMedInria\"
        )
    "
    )

install(CODE "
    execute_process(
        COMMAND \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/python${CMAKE_EXECUTABLE_SUFFIX}\"
        -m pip install \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/pyMedInria\"
        )
    file(GLOB
        bin_files
        LIST_DIRECTORIES FALSE
        \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/*\"
        )
    list(REMOVE_ITEM bin_files
        \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/pyMedInria${CMAKE_EXECUTABLE_SUFFIX}\"
        )
    if(bin_files)
        file(REMOVE \${bin_files})
    endif()
    "
    EXCLUDE_FROM_ALL
    COMPONENT Runtime
    )

if(APPLE)
    install(CODE "
        file(REMOVE_RECURSE \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks\")
        file(CREATE_LINK
            \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}\"
            \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks\"
            SYMBOLIC
            )
        "
        )

    install(CODE "
        file(REMOVE_RECURSE \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks\")
        file(RENAME
            \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}\"
            \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks\"
            )
        "
        EXCLUDE_FROM_ALL
        COMPONENT Runtime
        )
elseif(WIN32)

endif()
