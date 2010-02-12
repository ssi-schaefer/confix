PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_EXECUTABLE(executable main.c)

ADD_CUSTOM_TARGET(
    my-all-1
    ALL
    DEPENDS executable
    )

ADD_CUSTOM_TARGET(
    my-all-2
    ALL
    DEPENDS executable
    )
