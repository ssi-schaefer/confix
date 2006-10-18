dnl @synopsis AC_CXX_HAVE_LONG_LONG_FOR_IOSTREAM
dnl
dnl Check if the compiler allow long long for [i|o]stream Seems that
dnl OpenBSD / gcc-3 don't have it.
dnl
dnl Eg:
dnl
dnl   #include <iostream>
dnl   #ifdef HAVE_SSTREAM
dnl   #include <strstream>
dnl   #else
dnl   #include <sstream>
dnl   #endif
dnl   #ifdef HAVE_NAMESPACES
dnl   using namespace std;
dnl   #endif
dnl   ostream str((streambuf *)0);
dnl   long long lo=1;
dnl   str <<
dnl   #ifdef HAVE_LONG_LONG_FOR_IOSTREAM
dnl     (long int)
dnl   #endif
dnl           lo;
dnl
dnl @category Cxx
dnl @author Alain BARBET <alian@cpan.org>
dnl @version 2002-09-04
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_LONG_LONG_FOR_IOSTREAM],
[AC_CACHE_CHECK(whether the compiler allow long long for [i|o]stream,
ac_cv_cxx_have_ll_for_iostream,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_REQUIRE([AC_CXX_HAVE_SSTREAM])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <iostream>
#ifdef HAVE_SSTREAM
#include <strstream>
#else
#include <sstream>
#endif
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],[ ostream str((streambuf *)0); long long l=1; str << l; return 0;],
  ac_cv_cxx_have_ll_for_iostream=yes, ac_cv_cxx_have_ll_for_iostream=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_ll_for_iostream" = yes; then
   AC_DEFINE(HAVE_LONG_LONG_FOR_IOSTREAM,,[define if the compiler allow long long for [i|o]stream])
fi
])
