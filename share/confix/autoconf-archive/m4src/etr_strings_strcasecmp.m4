dnl @synopsis ETR_STRINGS_STRCASECMP
dnl
dnl This macro tries to find strcasecmp() in strings.h. See the
dnl ETR_STRING_STRCASECMP macro's commentary for usage details.
dnl
dnl @category C
dnl @author Warren Young <warren@etr-usa.com>
dnl @version 2001-05-25
dnl @license AllPermissive

AC_DEFUN([ETR_STRINGS_STRCASECMP],
[ AC_CACHE_CHECK([for strcasecmp() in strings.h], ac_cv_strings_strcasecmp, [

        AC_TRY_LINK(
                [ #include <strings.h> ],
                [ strcasecmp("foo", "bar"); ],
                ac_cv_strings_strcasecmp=yes,
                ac_cv_strings_strcasecmp=no)
])

        if test x"$ac_cv_strings_strcasecmp" = "xyes"
        then
                AC_DEFINE(HAVE_STRINGS_STRCASECMP, 1,
                        [ Define if your system has strcasecmp() in strings.h ])
        fi
]) dnl ETR_STRINGS_STRCASECMP
