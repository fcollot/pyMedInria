# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION ${CMAKE_MINIMUM_REQUIRED_VERSION})

################################################################################
# Project
################################################################################

set(MED_VERSION "${MED_VERSION_MAJOR}.${MED_VERSION_MINOR}.${MED_VERSION_PATCH}")

project(pyMedInria_library VERSION "${MED_VERSION}")

################################################################################
# CMake modules
################################################################################

include(CMakePackageConfigHelpers)

################################################################################
# Dependencies
################################################################################

find_package(pyncpp REQUIRED)

set(qt_components
    Core
    Widgets
    )

set(qt_libraries)

if(MED_USE_QT5)
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
#        set(library_dir "${MED_ROOT_BASE}/RelWithDebInfo/${MED_PYTHON_SUBDIR}/lib/site-packages")
#    else()
#        set(library_dir "${MED_ROOT_BASE}/RelWithDebInfo/${MED_PYTHON_SUBDIR}/lib/python${MED_PYTHON_VERSION_MAJOR}.${MED_PYTHON_VERSION_MINOR}/site-packages")
#    endif()

#    string(APPEND library_dir "/${MED_PYSIDE_PACKAGE}/Qt/lib")

#    list(APPEND qt_libraries "${library_dir}/${library}")
#endforeach()

#add_custom_command(
#    OUTPUT ${qt_libraries}
#    COMMAND pyMedInria_executable -m pip install ${MED_PYSIDE_PACKAGE}
#    VERBATIM
#    )

find_package(${MED_QT_PACKAGE} REQUIRED COMPONENTS ${qt_components})

################################################################################
# Files
################################################################################

set(headers
    pyMedInria.h
    pyMedInria/conversion.h
    pyMedInria/conversion/qobject.h
    )

set(sources
    pyMedInria/conversion/qobject.cpp
    )

################################################################################
# Library
################################################################################

set(target ${PROJECT_NAME})

add_library(${target} SHARED
    ${headers}
    ${sources}
    )

#add_dependencies(med_library_cpp med_python_packages)

################################################################################
# Target properties
################################################################################

#set_target_properties(med_library_cpp PROPERTIES
#    OUTPUT_NAME MusicBox
#    RUNTIME_OUTPUT_DIRECTORY "${MED_PACKAGE_ROOT}/musicbox/${MED_PACKAGE_RUNTIME_SUBDIR}"
#    LIBRARY_OUTPUT_DIRECTORY "${MED_PACKAGE_ROOT}/musicbox/${MED_PACKAGE_LIBRARY_SUBDIR}"
#    ARCHIVE_OUTPUT_DIRECTORY "${MED_PACKAGE_ROOT}/musicbox/${MED_PACKAGE_ARCHIVE_SUBDIR}"
#    )

################################################################################
# Compile definitions
################################################################################

target_compile_definitions(${target} PUBLIC
    MED_SHIBOKEN_PACKAGE="${MED_SIHBOKEN_PACKAGE}"
    )

################################################################################
# Includes
################################################################################

#set(qt_includes)

#foreach(component ${qt_components})
#    get_target_property(qt_include ${MED_QT_PACKAGE}::${component} INTERFACE_INCLUDE_DIRECTORIES)
#    list(APPEND qt_includes "${qt_include}")
#endforeach()

#list(REMOVE_DUPLICATES qt_includes)

target_include_directories(${target}
    PRIVATE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>/pyMedInria"
    PUBLIC
    #${qt_includes}
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
    "$<INSTALL_INTERFACE:include/pyMedInria>"
    )

################################################################################
# Link
################################################################################

#set(qt_libraries)

#if(MED_USE_QT5)
#    set(version_subdir 5)
#else()
#    set(version_subdir A)
#endif()

#foreach(component ${qt_components})
#    if(APPLE)
#        set(library "Qt${component}.framework/Versions/${version_subdir}/Qt${component}")
#    else()
#        set(library "Qt${component}${CMAKE_SHARED_LIBRARY_SUFFIX}")
#    endif()

#    if(WIN32)
#        set(library_dir "${MED_ROOT}/${MED_PYTHON_SUBDIR}/lib/site-packages")
#    else()
#        set(library_dir "${MED_ROOT}/${MED_PYTHON_SUBDIR}/lib/python${MED_PYTHON_VERSION_MAJOR}.${MED_PYTHON_VERSION_MINOR}/site-packages")
#    endif()

#    string(APPEND library_dir "/${MED_PYSIDE_PACKAGE}/Qt/lib")

#    list(APPEND qt_libraries "${library_dir}/${library}")
#endforeach()

target_link_libraries(${target} PUBLIC
    ${MED_QT_PACKAGE}::Core
    ${MED_QT_PACKAGE}::Widgets
    pyncpp_cpp_api
    )

#set_qt_paths(med_library_cpp)

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
# Config files
################################################################################

foreach(config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})

    configure_package_config_file("${CMAKE_CURRENT_SOURCE_DIR}/pyMedInriaConfig.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfig.cmake"
        INSTALL_PREFIX "/"
        INSTALL_DESTINATION "/${MED_SHARE_SUBDIR}"
        )

    write_basic_package_version_file("${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfigVersion.cmake"
        VERSION ${MED_VERSION}
        COMPATIBILITY SameMinorVersion
        )

    install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${config}/pyMedInriaConfigVersion.cmake"
        CONFIGURATIONS ${config}
        DESTINATION "${MED_SHARE_SUBDIR}"
        )

endforeach()

################################################################################
# Install/Export
################################################################################

install(TARGETS ${target}
    EXPORT ${target}_export
    COMPONENT Runtime
    )

install(EXPORT ${target}_export
    DESTINATION "${MED_SHARE_SUBDIR}"
    )

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/"
    DESTINATION "include/pyMedInria"
    FILES_MATCHING PATTERN "*.h"
    PATTERN "CMakeLists.txt" EXCLUDE
    )

