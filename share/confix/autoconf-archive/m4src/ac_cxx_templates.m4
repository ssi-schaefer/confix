dnl @synopsis AC_CXX_TEMPLATES
dnl
dnl If the compiler supports basic templates, define HAVE_TEMPLATES.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-04
dnl @license AllPermissive

AC_DEFUN([AC_CXX_TEMPLATES],
[AC_CACHE_CHECK(whether the compiler supports basic templates,
ac_cv_cxx_templates,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([template<class T> class A {public:A(){}};
template<class T> void f(const A<T>& ){}],[
A<double> d; A<int> i; f(d); f(i); return 0;],
 ac_cv_cxx_templates=yes, ac_cv_cxx_templates=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_templates" = yes; then
  AC_DEFINE(HAVE_TEMPLATES,,[define if the compiler supports basic templates])
fi
])
