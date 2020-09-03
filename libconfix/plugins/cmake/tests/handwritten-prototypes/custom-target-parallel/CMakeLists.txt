PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_CUSTOM_COMMAND(
    OUTPUT generated
    COMMAND sleep 1
    COMMAND echo custom command running
    COMMAND touch generated
    )

ADD_CUSTOM_TARGET(
    my-all-1
    ALL
    DEPENDS generated
    )

ADD_CUSTOM_TARGET(
    my-all-2
    ALL
    DEPENDS generated
    )

ADD_DEPENDENCIES(my-all-1 my-all-2)
