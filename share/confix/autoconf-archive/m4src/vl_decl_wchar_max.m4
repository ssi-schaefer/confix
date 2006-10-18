dnl @synopsis VL_DECL_WCHAR_MAX
dnl
dnl Checks whether the system headers define WCHAR_MAX or not. If it is
dnl already defined, does nothing. Otherwise checks the size and
dnl signedness of `wchar_t', and defines WCHAR_MAX to the maximum value
dnl that can be stored in a variable of type `wchar_t'.
dnl
dnl @category C
dnl @author Ville Laurikari <vl@iki.fi>
dnl @version 2002-04-04
dnl @license AllPermissive

AC_DEFUN([VL_DECL_WCHAR_MAX], [
  AC_CACHE_CHECK([whether WCHAR_MAX is defined], vl_cv_decl_wchar_max, [
    AC_TRY_COMPILE([
#ifdef HAVE_WCHAR_H
#include <wchar.h>
#endif
],[WCHAR_MAX],[vl_cv_decl_wchar_max="yes"],[vl_cv_decl_wchar_max="no"])])
  if test $vl_cv_decl_wchar_max = "no"; then
    VL_CHECK_SIGN([wchar_t],
      [ wc_signed="yes"
        AC_DEFINE(WCHAR_T_SIGNED, 1, [Define if wchar_t is signed]) ],
      [ wc_signed="no"
        AC_DEFINE(WCHAR_T_UNSIGNED, 1, [Define if wchar_t is unsigned])], [
#ifdef HAVE_WCHAR_H
#include <wchar.h>
#endif
])
    if test "$wc_signed" = "yes"; then
      AC_DEFINE(WCHAR_MAX, [(1L << (sizeof(wchar_t) * 8 - 1) - 1)], [
Define to the maximum value of wchar_t if not already defined elsewhere])
    elif test "$wc_signed" = "no"; then
      AC_DEFINE(WCHAR_MAX, [(1L << (sizeof(wchar_t) * 8) - 1)])
    fi
  fi
])dnl
