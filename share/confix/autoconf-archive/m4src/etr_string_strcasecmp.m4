dnl @synopsis ETR_STRING_STRCASECMP
dnl
dnl This macro tries to find strcasecmp() in string.h.
dnl
dnl Use this macro in conjunction with ETR_STRINGS_STRCASECMP in your
dnl configure.in like so:
dnl
dnl     ETR_STRING_STRCASECMP
dnl     if test x"$ac_cv_string_strcasecmp" = "xno" ; then
dnl         ETR_STRINGS_STRCASECMP
dnl     fi
dnl
dnl This will cause either HAVE_STRING_STRCASECMP or
dnl HAVE_STRINGS_STRCASECMP to be defined in config.h, which will tell
dnl your code what header to include to get strcasecmp()'s prototype.
dnl
dnl @category C
dnl @author Warren Young <warren@etr-usa.com>
dnl @version 2001-05-25
dnl @license AllPermissive

AC_DEFUN([ETR_STRING_STRCASECMP],
[
AC_CACHE_CHECK([for strcasecmp() in string.h], ac_cv_string_strcasecmp, [
        AC_TRY_LINK(
                [ #include <string.h> ],
                [ strcasecmp("foo", "bar"); ],
                ac_cv_string_strcasecmp=yes,
                ac_cv_string_strcasecmp=no)
])

        if test x"$ac_cv_string_strcasecmp" = "xyes"
        then
                AC_DEFINE(HAVE_STRING_STRCASECMP, 1,
                        [ Define if your system has strcasecmp() in string.h ])
        fi
]) dnl ETR_STRING_STRCASECMP
