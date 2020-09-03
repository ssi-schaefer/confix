dnl @synopsis AC_CXX_LDFLAGS_STD_LANG(LD-FLAGS)
dnl
dnl Append to LD-FLAGS the set of link-time flags that should be passed
dnl to the C++ compiler in order to enable use of C++ features as
dnl defined in the ANSI C++ standard (eg. use of standard iostream
dnl classes in the `std' namespace, etc.). Note that if you use GNU
dnl Libtool you may need to prefix each of those switches with
dnl `-Xlinker' so that Libtool doesn't discard them (see Libtool's
dnl manual and `AC_LIBTOOLIZE_LDFLAGS').
dnl
dnl @category Cxx
dnl @author Ludovic Courtès <ludo@chbouib.org>
dnl @version 2004-09-07
dnl @license AllPermissive

AC_DEFUN([AC_CXX_LDFLAGS_STD_LANG],
  [AC_REQUIRE([AC_CXX_COMPILER_VENDOR])
   case "$ac_cv_cxx_compiler_vendor" in
     sgi)    $1="$$1 -LANG:std -exceptions";;
     hp)     $1="$$1 -AA";;
   esac])
