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

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/setup.py"
    "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    @ONLY)

if(UNIX OR MED_SYMLINK_SOURCE_PACKAGE)
    set(link_command create_symlink)
else()
    set(link_command copy_directory)
endif()

add_custom_target(${PROJECT_NAME}_package ALL
    COMMAND ${CMAKE_COMMAND} -E rm -rf pymedinria
    COMMAND ${CMAKE_COMMAND} -E ${link_command} "${CMAKE_CURRENT_SOURCE_DIR}/pymedinria" pymedinria
    COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CMAKE_CURRENT_BINARY_DIR}/setup.py" .
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    VERBATIM
    )

################################################################################
# Virtual env
################################################################################

if(MED_BUILD_PYTHON)

#    add_custom_target(${PROJECT_NAME}_install_package ALL
#        COMMAND "${pyncpp_EXECUTABLE}" -m ensurepip
#        COMMAND "${pyncpp_EXECUTABLE}" -m pip install -e "${MED_ROOT}/package"
#        VERBATIM
#        )

#    add_dependencies(${PROJECT_NAME}_install_package ${PROJECT_NAME}_package)

    ############################################################################
    # Runner targets
    ############################################################################

#    add_custom_target(med_run_application
#        COMMAND "${Python_EXECUTABLE}" -m pymedinria
#        VERBATIM
#        )

#    add_dependencies(med_run_application med_install_packages)

#    add_custom_target(med_run_tests
#        COMMAND "${Python_EXECUTABLE}" -m pymedinria --test
#        VERBATIM
#        )

#    add_dependencies(med_run_tests med_install_packages)
    
    ############################################################################
    # Distribution
    ############################################################################

#    add_custom_target(med_build_distribution ALL
#        COMMAND "${Python_EXECUTABLE}" -m build "${MED_PACKAGE_ROOT}/pymedinria"
#        VERBATIM
#        )
        
#    add_dependencies(med_build_distribution med_install_packages)

    ############################################################################
    # CTest
    ############################################################################

#    add_test(NAME ${PROJECT_NAME}_no_gui
#        COMMAND "${Python_EXECUTABLE}" -m pymedinria --test no-gui
#        )

#    add_test(NAME ${PROJECT_NAME}_gui
#        COMMAND "${Python_EXECUTABLE}" -m pymedinria --test gui
#        )

#    set_property(TEST ${PROJECT_NAME}_no_gui PROPERTY LABELS TEST_NO_GUI)
#    set_property(TEST ${PROJECT_NAME}_gui PROPERTY LABELS TEST_GUI)

endif()

################################################################################
# Install
################################################################################

if(MED_BUILD_PYTHON)
    install(CODE "
        execute_process(
            COMMAND \"${pyncpp_EXECUTABLE}\" -m ensurepip
            COMMAND \"${pyncpp_EXECUTABLE}\" -m pip install -e \"${CMAKE_CURRENT_BINARY_DIR}\"
            )
        "
        COMPONENT Runtime
        )
endif()
