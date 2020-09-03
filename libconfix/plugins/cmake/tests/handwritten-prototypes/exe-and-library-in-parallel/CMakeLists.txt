PROJECT(test)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

ADD_EXECUTABLE(executable main.c file.c)
ADD_LIBRARY(library file.c)
