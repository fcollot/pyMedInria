# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Project
################################################################################

project(${PROJECT_NAME}_packaging VERSION "${PROJECT_VERSION}")

################################################################################
# CPack
################################################################################

#set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${CPACK_PACKAGE_NAME} - medical image visualisation and processing tool")

#set(CPACK_PACKAGE_DESCRIPTION
#    "${CPACK_PACKAGE_NAME} is a cardiac image visualization and processing tool developed in collaboration between INRIA and the IHU LIRYC.")

#set(CPACK_PACKAGE_VENDOR  https://www.ihu-liryc.fr/fr/music/)
#set(CPACK_PACKAGE_CONTACT "MUSICardio Team <music@inria.fr>")

#set(CPACK_PACKAGE_VERSION_MAJOR ${${PROJECT_NAME}_VERSION_MAJOR})
#set(CPACK_PACKAGE_VERSION_MINOR ${${PROJECT_NAME}_VERSION_MINOR})
#set(CPACK_PACKAGE_VERSION_PATCH ${${PROJECT_NAME}_VERSION_PATCH})
#set(CPACK_PACKAGE_VERSION ${${PROJECT_NAME}_VERSION})

#set(CPACK_PACKAGE_DESCRIPTION_FILE "${PROJECT_SOURCE_DIR}/Description.txt")
#set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE_MUSICardio.txt")
#set(CPACK_RESOURCE_FILE_README "${PROJECT_SOURCE_DIR}/Readme.txt")
#set(CPACK_RESOURCE_FILE_WELCOME "${PROJECT_SOURCE_DIR}/Welcome.txt")

set(CPACK_BINARY_STGZ OFF)
set(CPACK_BINARY_TBZ2 OFF)
set(CPACK_BINARY_TGZ ON)
set(CPACK_BINARY_TZ OFF)

set(CPACK_INSTALL_CMAKE_PROJECTS ${PROJECT_BINARY_DIR} ${PROJECT_NAME} Package "/")

install(CODE "
    execute_process(
        COMMAND ${CMAKE_COMMAND}
        --install \"${CMAKE_BINARY_DIR}\"
        --prefix \"\${CMAKE_INSTALL_PREFIX}\"
        --component Runtime
        )
    "
    EXCLUDE_FROM_ALL
    COMPONENT Package
    )

include(CPack)
