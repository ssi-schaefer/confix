ADD_CUSTOM_TARGET(
    custom
    ALL
    COMMAND echo executing custom target ...
    DEPENDS generated.h
    )

ADD_CUSTOM_COMMAND(
    OUTPUT generated.h
    COMMAND echo generating generated.h ...
    COMMAND touch generated.h
    )
