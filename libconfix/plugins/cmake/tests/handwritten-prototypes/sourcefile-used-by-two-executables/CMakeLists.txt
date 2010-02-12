PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_CUSTOM_COMMAND(
    OUTPUT generated-main.c
    COMMAND echo custom command enter
    COMMAND sleep 1
    COMMAND echo 'int main() {}' > generated-main.c
    COMMAND echo custom command leave
    )

ADD_CUSTOM_TARGET(
    hack
    DEPENDS generated-main.c
    )

ADD_EXECUTABLE(executable1 generated-main.c)
ADD_DEPENDENCIES(executable1 hack)

ADD_EXECUTABLE(executable2 generated-main.c)
ADD_DEPENDENCIES(executable2 hack)
