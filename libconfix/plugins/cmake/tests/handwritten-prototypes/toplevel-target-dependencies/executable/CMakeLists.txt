INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/library)
ADD_EXECUTABLE(main main.c)
TARGET_LINK_LIBRARIES(main library)

ADD_CUSTOM_TARGET(
    main-custom
    ALL
    )

ADD_DEPENDENCIES(main-custom main)
