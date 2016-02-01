
include_directories(
    ${Boost_INCLUDE_DIRS}
    ${OCC_INCLUDE_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${ZLIB_INCLUDE_DIR}
    ${XercesC_INCLUDE_DIRS}
)

set(OptElements_LIBS
    FreeCADApp
)

SET(OptElements_SRCS
    AppOptElements.cpp
    AppOptElementsPy.cpp
    PreCompiled.cpp
    PreCompiled.h
)

add_library(OptElements SHARED ${OptElements_SRCS})
target_link_libraries(OptElements ${OptElements_LIBS})


fc_target_copy_resource(OptElements 
    ${CMAKE_SOURCE_DIR}/src/Mod/OptElements
    ${CMAKE_BINARY_DIR}/Mod/OptElements
    Init.py)

SET_BIN_DIR(OptElements OptElements /Mod/OptElements)
SET_PYTHON_PREFIX_SUFFIX(OptElements)

install(TARGETS OptElements DESTINATION ${CMAKE_INSTALL_LIBDIR})
