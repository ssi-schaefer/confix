dnl @synopsis AC_CXX_HAVE_EXT_HASH_SET
dnl
dnl Check if the compiler has ext/hash_set Eg:
dnl
dnl   #if defined(HAVE_EXT_HASH_SET)
dnl   #include <ext/hash_set>
dnl   #else
dnl   #if defined(HAVE_STL)
dnl   #include <hash_set>
dnl   #else
dnl   # Can't find hash_set header !
dnl   #endif
dnl   #endif
dnl
dnl @category Cxx
dnl @author Alain BARBET <alian@cpan.org>
dnl @version 2002-09-04
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_EXT_HASH_SET],
[AC_CACHE_CHECK(whether the compiler has ext/hash_set,
ac_cv_cxx_have_ext_hash_set,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <ext/hash_set>
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],[hash_set<int> t; return 0;],
  ac_cv_cxx_have_ext_hash_set=yes, ac_cv_cxx_have_ext_hash_set=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_ext_hash_set" = yes; then
   AC_DEFINE(HAVE_EXT_HASH_SET,,[define if the compiler has ext/hash_set])
fi
])
