dnl @synopsis AC_PROTOTYPE_SETSOCKOPT
dnl
dnl Requires the AC_PROTOTYPE macro.
dnl
dnl Find the type of argument three of setsockopt. User must include
dnl the following in acconfig.h:
dnl
dnl /* Type of third argument of setsockopt */ #undef SETSOCKOPT_ARG3
dnl
dnl @category Misc
dnl @author Loic Dachary <loic@senga.org>
dnl @version 2000-08-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROTOTYPE_SETSOCKOPT],[
AC_PROTOTYPE(setsockopt,
 [
  #include <sys/types.h>
  #include <sys/socket.h>
 ],
 [
  int a = 0;
  ARG3 b = 0;
  setsockopt(a, SOL_SOCKET, SO_REUSEADDR, b, sizeof(a));
 ],
 ARG3, [const void*, const char*, void*, char*])
])
