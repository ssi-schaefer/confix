dnl @synopsis AC_CXX_OLD_FOR_SCOPING
dnl
dnl If the compiler accepts the old for scoping rules (the scope of a
dnl variable declared inside the parentheses extends outside the
dnl for-body), define HAVE_OLD_FOR_SCOPING. Note that some compilers
dnl (notably g++ and egcs) support both new and old rules since they
dnl accept the old rules and only generate a warning.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_OLD_FOR_SCOPING],
[AC_CACHE_CHECK(whether the compiler accepts the old for scoping rules,
ac_cv_cxx_old_for_scoping,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE(,[int z;for (int i=0; i < 10; ++i)z=z+i;z=i;return z;],
 ac_cv_cxx_old_for_scoping=yes, ac_cv_cxx_old_for_scoping=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_old_for_scoping" = yes; then
  AC_DEFINE(HAVE_OLD_FOR_SCOPING,,[define if the compiler accepts the old for scoping rules])
fi
])
