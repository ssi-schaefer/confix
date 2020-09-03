dnl @synopsis AX_REQUIRE_ONE_FUNC (FUNCTION..., [ACTION-IF-ANY-FOUND], [ACTION-IF-NONE-FOUND])
dnl
dnl AX_REQUIRE_ONE_FUNC is a simple wrapper for AC_CHECK_FUNCS. It
dnl calls AC_CHECK_FUNCS on the list of functions named in the first
dnl argument, then invokes ACTION-IF-ANY-FOUND if at least one of the
dnl functions exists or ACTION-IF-NONE-FOUND if none of the functions
dnl exist.
dnl
dnl Here's an example:
dnl
dnl     AX_REQUIRE_ONE_FUNC([posix_memalign memalign valloc], ,
dnl       [AC_MSG_ERROR([unable to allocate page-aligned memory])])
dnl
dnl @category Misc
dnl @author Scott Pakin <pakin@uiuc.edu>
dnl @version 2005-01-22
dnl @license AllPermissive

AC_DEFUN([AX_REQUIRE_ONE_FUNC],
[m4_define([ax_1func_cv], [AS_TR_SH(ax_cv_func_any_$1)])
AC_CACHE_VAL([ax_1func_cv],
  [ax_1func_cv=no
   AC_CHECK_FUNCS([$1], [ax_1func_cv="$ax_1func_cv $ac_func"])])
AS_IF([test "$ax_1func_cv" = "no"],
  [$3],
  [ax_1func_cv=`echo $ax_1func_cv | sed 's/^no //'`
   $2])
])
