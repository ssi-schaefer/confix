INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/library)
ADD_EXECUTABLE(main2 main2.c)

ADD_CUSTOM_TARGET(
    main2-custom
    ALL
    )

ADD_DEPENDENCIES(main2-custom main)
ADD_DEPENDENCIES(main custom)
