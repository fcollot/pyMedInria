# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

################################################################################
# Project
################################################################################

set(MED_VERSION "${MED_VERSION_MAJOR}.${MED_VERSION_MINOR}.${MED_VERSION_PATCH}")

project(pyMedInria_standalone VERSION "${MED_VERSION}")

################################################################################
# Dependencies
################################################################################

find_package(pyMedInria REQUIRED)

#set(qt_components
#    Core
#    Widgets
#    )

#set(qt_libraries)

if(MED_QT_PACKAGE EQUAL 5)
    set(qt_version_subdir 5)
else()
    set(qt_version_subdir A)
endif()

#foreach(component ${qt_components})
#    if(APPLE)
#        set(library "Qt${component}.framework/Versions/${version_subdir}/Qt${component}")
#    else()
#        set(library "Qt${component}${CMAKE_SHARED_LIBRARY_SUFFIX}")
#    endif()

#    if(WIN32)
#        set(library_dir "${MED_ROOT_BASE}/RelWithDebInfo/${PYNCPP_PYTHON_SUBDIR}/lib/site-packages")
#    else()
#        set(library_dir "${MED_ROOT_BASE}/RelWithDebInfo/${PYNCPP_PYTHON_SUBDIR}/lib/python${PYNCPP_PYTHON_VERSION_MAJOR}.${PYNCPP_PYTHON_VERSION_MINOR}/site-packages")
#    endif()

#    string(APPEND library_dir "/${MED_PYSIDE_PACKAGE}/Qt/lib")

#    list(APPEND qt_libraries "${library_dir}/${library}")
#endforeach()

#add_custom_command(
#    OUTPUT ${qt_libraries}
#    COMMAND pyncpp_executable -m pip install ${MED_PYSIDE_PACKAGE}
#    VERBATIM
#    )

#find_package(${MED_QT_PACKAGE} REQUIRED COMPONENTS ${qt_components})

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

add_executable(${target} WIN32
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
        set(bin_dir "${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/MacOS")
        set(lib_dir "${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks")
    else()
        set(bin_dir "${CMAKE_INSTALL_BINDIR}")
        set(lib_dir "${CMAKE_INSTALL_LIBDIR}")
    endif()

    file(RELATIVE_PATH relative_lib_dir "/${bin_dir}" "/${lib_dir}")
    list(APPEND rpath "${rpath_prefix}/${relative_lib_dir}")

    if(APPLE)
        set(qt_lib_dir "${CMAKE_INSTALL_BINDIR}/pyMedInria.app/Contents/Frameworks")
    else()
        set(qt_lib_dir "${CMAKE_INSTALL_LIBDIR}")
    endif()

    string(APPEND qt_lib_dir "/${pyncpp_PYTHON_SUBDIR}/site-packages/${MED_PYSIDE_PACKAGE}/Qt/lib")

    file(RELATIVE_PATH relative_qt_lib_dir "/${bin_dir}" "/${qt_lib_dir}")
    list(APPEND rpath "${rpath_prefix}/${relative_qt_lib_dir}")

    set_target_properties(${target} PROPERTIES
        INSTALL_RPATH "${rpath}"
        )
endif()

set_target_properties(${target} PROPERTIES
    OUTPUT_NAME pyMedInria
    )

if(APPLE)
    set_target_properties(${target} PROPERTIES
        MACOSX_BUNDLE TRUE
        )
endif()

################################################################################
# Compile definitions
################################################################################

if(APPLE)
    set(lib_dir "Frameworks")
else()
    set(lib_dir "${CMAKE_INSTALL_LIBDIR}")
endif()

target_compile_definitions(${target} PUBLIC
    PYTHON_HOME=".."
    PYTHON_LIB_DIR="${lib_dir}"
    )

################################################################################
# Link
################################################################################

target_link_libraries(${target} PUBLIC
    pyMedInria_library
    )

if(APPLE)
    add_custom_command(TARGET ${target} POST_BUILD
        COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
        $<TARGET_FILE:${MED_QT_PACKAGE}::Core>
        "@rpath/QtCore.framework/Versions/${qt_version_subdir}/QtCore"
        $<TARGET_FILE:${target}>
        COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
        $<TARGET_FILE:${MED_QT_PACKAGE}::Widgets>
        "@rpath/QtWidgets.framework/Versions/${qt_version_subdir}/QtWidgets"
        $<TARGET_FILE:${target}>
        COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
        $<TARGET_FILE:${MED_QT_PACKAGE}::Gui>
        "@rpath/QtGui.framework/Versions/${qt_version_subdir}/QtGui"
        $<TARGET_FILE:${target}>
        VERBATIM
        )
endif()

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
        COMMAND ./python${CMAKE_EXECUTABLE_SUFFIX} -m ensurepip
        COMMAND ./python${CMAKE_EXECUTABLE_SUFFIX} -m pip install -e \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/pyMedInria\"
        WORKING_DIRECTORY \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}\"
        )
    "
    )

install(CODE "
    execute_process(
        COMMAND ./python${CMAKE_EXECUTABLE_SUFFIX} -m ensurepip
        COMMAND ./python${CMAKE_EXECUTABLE_SUFFIX} -m pip install \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/pyMedInria\"
        WORKING_DIRECTORY \"\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}\"
        )
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
endif()
