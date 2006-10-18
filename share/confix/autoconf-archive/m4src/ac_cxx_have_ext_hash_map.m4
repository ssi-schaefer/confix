dnl @synopsis AC_CXX_HAVE_EXT_HASH_MAP
dnl
dnl Check if the compiler has ext/hash_map Eg:
dnl
dnl   #if defined(HAVE_EXT_HASH_MAP)
dnl   #include <ext/hash_map>
dnl   #else
dnl   #if defined(HAVE_STL)
dnl   #include <hash_map>
dnl   #else
dnl   # Can't find hash_map header !
dnl   #endif
dnl   #endif
dnl
dnl This file is Alain BARBET's AC_CXX_HAVE_EXT_HASH_SET 1.1 with
dnl s/set/map/g :)
dnl
dnl @category Cxx
dnl @author Perceval ANICHINI <perceval.anichini@epita.fr>
dnl @version 2002-09-25
dnl @license GPLWithACException

AC_DEFUN([AC_CXX_HAVE_EXT_HASH_MAP],
[AC_CACHE_CHECK(whether the compiler has ext/hash_map,
ac_cv_cxx_have_ext_hash_map,
[AC_REQUIRE([AC_CXX_NAMESPACES])
  AC_LANG_SAVE
  AC_LANG_CPLUSPLUS
  AC_TRY_COMPILE([#include <ext/hash_map>
#ifdef HAVE_NAMESPACES
using namespace std;
#endif],[hash_map<int, int> t; return 0;],
  ac_cv_cxx_have_ext_hash_map=yes, ac_cv_cxx_have_ext_hash_map=no)
  AC_LANG_RESTORE
])
if test "$ac_cv_cxx_have_ext_hash_map" = yes; then
   AC_DEFINE(HAVE_EXT_HASH_MAP,,[define if the compiler has ext/hash_map])
fi
])
