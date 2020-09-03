dnl @synopsis AC_CXX_HAVE_EMPTY_IOSTREAM
dnl
dnl Check if the compiler allow the empty iostream constructor. Ok
dnl before gcc3, not after.
dnl
dnl @category Cxx
dnl @author Alain BARBET <alian@cpan.org>
dnl @version 2003-04-09
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_EMPTY_IOSTREAM],
[AC_CACHE_CHECK(whether the compiler allow empty iostream,
ac_cv_cxx_have_empty_iostream,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <iostream>
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],[iostream iostr; return 0;],
  ac_cv_cxx_have_empty_iostream=yes, ac_cv_cxx_have_empty_iostream=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_empty_iostream" = yes; then
   AC_DEFINE(HAVE_EMPTY_IOSTREAM,,[define if the compiler allow empty
iostream])
fi
])
