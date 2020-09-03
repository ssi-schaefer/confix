ADD_LIBRARY(library library.h library.c)
ADD_DEPENDENCIES(library custom)

INCLUDE_DIRECTORIES(${CMAKE_BINARY_DIR}/custom)

ADD_CUSTOM_TARGET(
    library-custom
    ALL
    )

ADD_DEPENDENCIES(library-custom library)
