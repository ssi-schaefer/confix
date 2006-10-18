dnl @synopsis AC_CXX_MUTABLE
dnl
dnl If the compiler allows modifying class data members flagged with
dnl the mutable keyword even in const objects (for example in the body
dnl of a const member function), define HAVE_MUTABLE.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_MUTABLE],
[AC_CACHE_CHECK(whether the compiler supports the mutable keyword,
ac_cv_cxx_mutable,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([
class A { mutable int i;
          public:
          int f (int n) const { i = n; return i; }
        };
],[A a; return a.f (1);],
 ac_cv_cxx_mutable=yes, ac_cv_cxx_mutable=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_mutable" = yes; then
  AC_DEFINE(HAVE_MUTABLE,,[define if the compiler supports the mutable keyword])
fi
])
