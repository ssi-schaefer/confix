PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_CUSTOM_COMMAND(
    OUTPUT generated
    COMMAND sh -c "(echo \"fut\")|grep fut"
    COMMAND touch generated
    VERBATIM
    )

ADD_CUSTOM_TARGET(
    my-all-1
    ALL
    DEPENDS generated
    )
