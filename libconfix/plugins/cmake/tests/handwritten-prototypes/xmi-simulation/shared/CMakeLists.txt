ADD_CUSTOM_COMMAND(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/shared-c.c ${CMAKE_CURRENT_BINARY_DIR}/shared-c.h ${CMAKE_CURRENT_BINARY_DIR}/template-somefile
    COMMAND sleep 1
    COMMAND touch ${CMAKE_CURRENT_BINARY_DIR}/shared-c.c ${CMAKE_CURRENT_BINARY_DIR}/shared-c.h ${CMAKE_CURRENT_BINARY_DIR}/template-somefile
    VERBATIM
)

ADD_LIBRARY(
    shared
    ${CMAKE_CURRENT_BINARY_DIR}/shared-c.c
    ${CMAKE_CURRENT_BINARY_DIR}/shared-c.h
)

ADD_CUSTOM_TARGET(
    my-all-target
    ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/template-somefile
)

# ADD_CUSTOM_COMMAND(
#     OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/somefile1
#     COMMAND cp ${CMAKE_CURRENT_BINARY_DIR}/template-somefile ${CMAKE_CURRENT_BINARY_DIR}/somefile1
#     DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/template-somefile
#     VERBATIM
# )
# 
# ADD_CUSTOM_TARGET(
#     somefile1-target
#     ALL
#     DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/somefile1
# )
# 
# ADD_CUSTOM_COMMAND(
#     OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/somefile2
#     COMMAND cp ${CMAKE_CURRENT_BINARY_DIR}/template-somefile ${CMAKE_CURRENT_BINARY_DIR}/somefile2
#     DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/template-somefile
#     VERBATIM
# )
# 
# ADD_CUSTOM_TARGET(
#     somefile2-target
#     ALL
#     DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/somefile2
# )

# ADD_DEPENDENCIES(
#     somefile2-target
#     somefile1-target
# )
# 
# ADD_DEPENDENCIES(
#     somefile1-target
#     shared
# )
