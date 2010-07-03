PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_CUSTOM_COMMAND(
    OUTPUT command-file
    COMMAND rm ARGS -f command-file
    # goal is to print out, literally, including quotes: "blah(bloh)" > < '
    COMMAND echo ARGS echo \\\\\"blah\\\\\(bloh\\\\\)\\\\\" \\\\> \\\\< \\\\' >> command-file
    COMMAND echo ARGS touch file.h >> command-file
    VERBATIM
    )

ADD_CUSTOM_COMMAND(
    OUTPUT file.h
    DEPENDS command-file
    COMMAND sh -c "while read cmd; do eval \$cmd || exit 1; done" < command-file
    VERBATIM
    )

ADD_CUSTOM_TARGET(
    hook-file.h-to-all
    ALL
    DEPENDS file.h
    )
