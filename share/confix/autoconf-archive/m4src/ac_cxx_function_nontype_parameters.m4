dnl @synopsis AC_CXX_FUNCTION_NONTYPE_PARAMETERS
dnl
dnl If the compiler supports function templates with non-type
dnl parameters, define HAVE_FUNCTION_NONTYPE_PARAMETERS.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_FUNCTION_NONTYPE_PARAMETERS],
[AC_CACHE_CHECK(whether the compiler supports function templates with non-type parameters,
ac_cv_cxx_function_nontype_parameters,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([
template<class T, int N> class A {};
template<class T, int N> int f(const A<T,N>& x) { return 0; }
],[A<double, 17> z; return f(z);],
 ac_cv_cxx_function_nontype_parameters=yes, ac_cv_cxx_function_nontype_parameters=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_function_nontype_parameters" = yes; then
  AC_DEFINE(HAVE_FUNCTION_NONTYPE_PARAMETERS,,
            [define if the compiler supports function templates with non-type parameters])
fi
])
