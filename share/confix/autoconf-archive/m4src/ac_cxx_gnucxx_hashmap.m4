dnl @synopsis AC_CXX_GNUCXX_HASHMAP
dnl
dnl Test for the presence of GCC's hashmap STL extension.
dnl
dnl @category Cxx
dnl @author Patrick Mauritz <oxygene@studentenbude.ath.cx>
dnl @version 2005-07-18
dnl @license AllPermissive

AC_DEFUN([AC_CXX_GNUCXX_HASHMAP],[
AC_CACHE_CHECK(whether the compiler supports __gnu_cxx::hash_map,
ac_cv_cxx_gnucxx_hashmap,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([#include <ext/hash_map>
using __gnu_cxx::hash_map;],
 [],
 ac_cv_cxx_gnucxx_hashmap=yes, ac_cv_cxx_gnucxx_hashmap=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_gnucxx_hashmap" = yes; then
  AC_DEFINE(HAVE_GNUCXX_HASHMAP,,[define if the compiler supports __gnu_cxx::hash_map])
fi
])
