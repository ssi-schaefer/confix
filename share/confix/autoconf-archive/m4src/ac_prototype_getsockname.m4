dnl @synopsis AC_PROTOTYPE_GETSOCKNAME
dnl
dnl Requires the AC_PROTOTYPE macro.
dnl
dnl Find the type of argument two and three of getsockname. User must
dnl include the following in acconfig.h:
dnl
dnl /* Type of second argument of getsockname */ #undef
dnl GETSOCKNAME_ARG2
dnl
dnl /* Type of third argument of getsockname */ #undef GETSOCKNAME_ARG3
dnl
dnl @category Misc
dnl @author Loic Dachary <loic@senga.org>
dnl @version 2000-08-11
dnl @license GPLWithACException

AC_DEFUN([AC_PROTOTYPE_GETSOCKNAME],[
AC_PROTOTYPE(getsockname,
 [
  #include <sys/types.h>
  #include <sys/socket.h>
 ],
 [
  int a = 0;
  ARG2 * b = 0;
  ARG3 * c = 0;
  getsockname(a, b, c);
 ],
 ARG2, [struct sockaddr, void],
 ARG3, [socklen_t, size_t, int, unsigned int, long unsigned int])
])
