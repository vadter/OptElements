
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_CURRENT_BINARY_DIR}
    ${Boost_INCLUDE_DIRS}
    ${COIN3D_INCLUDE_DIRS}
    ${QT_INCLUDE_DIR}
    ${ZLIB_INCLUDE_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${XercesC_INCLUDE_DIRS}
)

set(OptElementsGui_LIBS
    OptElements
    FreeCADGui
)

qt4_add_resources(OptElements_QRC_SRCS Resources/OptElements.qrc)

SET(OptElementsGui_SRCS
    ${OptElements_QRC_SRCS}
    AppOptElementsGui.cpp
    AppOptElementsGuiPy.cpp
    Command.cpp
    PreCompiled.cpp
    PreCompiled.h
    Workbench.cpp
    Workbench.h
)

add_library(OptElementsGui SHARED ${OptElementsGui_SRCS})
target_link_libraries(OptElementsGui ${OptElementsGui_LIBS})

fc_target_copy_resource(OptElementsGui 
    ${CMAKE_SOURCE_DIR}/src/Mod/OptElements
    ${CMAKE_BINARY_DIR}/Mod/OptElements
    InitGui.py)

SET_BIN_DIR(OptElementsGui OptElementsGui /Mod/OptElements)
SET_PYTHON_PREFIX_SUFFIX(OptElementsGui)
    
install(TARGETS OptElementsGui DESTINATION ${CMAKE_INSTALL_LIBDIR})
