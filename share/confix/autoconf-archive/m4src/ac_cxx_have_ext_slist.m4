dnl @synopsis AC_CXX_HAVE_EXT_SLIST
dnl
dnl Check if the compiler has ext/slist. Eg:
dnl
dnl   #if defined(HAVE_EXT_SLIST)
dnl   #include <ext/slist>
dnl   #else
dnl   #if defined(HAVE_STL)
dnl   #include <slist>
dnl   #else
dnl   # Can't find slist header !
dnl   #endif
dnl   #endif
dnl
dnl @category Cxx
dnl @author Alain BARBET <alian@cpan.org>
dnl @version 2002-09-04
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_EXT_SLIST],
[AC_CACHE_CHECK(whether the compiler has ext/slist,
ac_cv_cxx_have_ext_slist,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <ext/slist>
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],[slist<int> s; return 0;],
  ac_cv_cxx_have_ext_slist=yes, ac_cv_cxx_have_ext_slist=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_ext_slist" = yes; then
   AC_DEFINE(HAVE_EXT_SLIST,,[define if the compiler has ext/slist])
fi
])
