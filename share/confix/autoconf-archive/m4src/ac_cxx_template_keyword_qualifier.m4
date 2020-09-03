dnl @synopsis AC_CXX_TEMPLATE_KEYWORD_QUALIFIER
dnl
dnl If the compiler supports use of the template keyword as a
dnl qualifier, define HAVE_TEMPLATE_KEYWORD_QUALIFIER.
dnl
dnl @category Cxx
dnl @author Todd Veldhuizen
dnl @author Bernardo Innocenti
dnl @author Luc Maisonobe <luc@spaceroots.org>
dnl @version 2004-02-06
dnl @license AllPermissive

AC_DEFUN([AC_CXX_TEMPLATE_KEYWORD_QUALIFIER],
[AC_CACHE_CHECK(whether the compiler supports use of the template keyword as a qualifier,
ac_cv_cxx_template_keyword_qualifier,
[AC_LANG_SAVE
 AC_LANG_CPLUSPLUS
 AC_TRY_COMPILE([
  class X
  {
    public:
    template<int> void member() {}
    template<int> static void static_member() {}
  };
  template<class T> void f(T* p)
  {
    p->template member<200>(); // OK: < starts template argument
    T::template static_member<100>(); // OK: < starts explicit qualification
  }
],[X x; f(&x); return 0;],
 ac_cv_cxx_template_keyword_qualifier=yes, ac_cv_cxx_template_keyword_qualifier=no)
 AC_LANG_RESTORE
])
if test "$ac_cv_cxx_template_keyword_qualifier" = yes; then
  AC_DEFINE(HAVE_TEMPLATE_KEYWORD_QUALIFIER,,
            [define if the compiler supports use of the template keyword as a qualifier])
fi
])
