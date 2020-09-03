dnl @synopsis AC_CXX_CXXFLAGS_STD_LANG(CXX-FLAGS)
dnl
dnl Append to variable CXX-FLAGS the set of compile-time flags that
dnl should be passed to the C++ compiler in order to enable use of C++
dnl features as defined in the ANSI C++ standard (eg. use of standard
dnl iostream classes in the `std' namespace, etc.). Note that if you
dnl use GNU Libtool you may need to prefix each of those flags with
dnl `-Xcompiler' so that Libtool doesn't discard them (see Libtool's
dnl manual and `AC_LIBTOOLIZE_CFLAGS').
dnl
dnl @category Cxx
dnl @author Ludovic Courtès <ludo@chbouib.org>
dnl @version 2004-09-07
dnl @license AllPermissive

AC_DEFUN([AC_CXX_CXXFLAGS_STD_LANG],
  [AC_REQUIRE([AC_CXX_COMPILER_VENDOR])
   case "$ac_cv_cxx_compiler_vendor" in
     sgi)    $1="$$1 -LANG:std -exceptions";;
     hp)     $1="$$1 -AA";;
   esac])
