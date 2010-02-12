ADD_CUSTOM_COMMAND(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/generated.h
    COMMAND touch ${CMAKE_CURRENT_BINARY_DIR}/generated.h
)

ADD_CUSTOM_TARGET(
    __my__generated__
    ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/generated.h
)
