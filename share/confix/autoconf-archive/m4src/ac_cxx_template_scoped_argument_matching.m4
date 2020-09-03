dnl @synopsis AC_CXX_TEMPLATE_SCOPED_ARGUMENT_MATCHING
dnl
dnl If the compiler supports function matching with argument types
dnl which are template scope-qualified, define
dnl HAVE_TEMPLATE_SCOPED_ARGUMENT_MATCHING.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_TEMPLATE_SCOPED_ARGUMENT_MATCHING],
[AC_CACHE_CHECK(whether the compiler supports function matching with argument types which are template scope-qualified,
ac_cv_cxx_template_scoped_argument_matching,
[AC_REQUIRE([AC_CXX_TYPENAME])
 AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([
#ifndef HAVE_TYPENAME
 #define typename
#endif
template<class X> class A { public : typedef X W; };
template<class Y> class B {};
template<class Y> void operator+(B<Y> d1, typename Y::W d2) {}
],[B<A<float> > z; z + 0.5f; return 0;],
 ac_cv_cxx_template_scoped_argument_matching=yes, ac_cv_cxx_template_scoped_argument_matching=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_template_scoped_argument_matching" = yes; then
  AC_DEFINE(HAVE_TEMPLATE_SCOPED_ARGUMENT_MATCHING,,
            [define if the compiler supports function matching with argument types which are template scope-qualified])
fi
])
