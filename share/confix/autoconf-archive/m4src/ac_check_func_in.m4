dnl @synopsis AC_CHECK_FUNC_IN(HEADER, FUNCTION [,ACTION-IF-FOUNC [,ACTION-IF-NOT-FOUND]])
dnl
dnl Checking for library functions in a given header file
dnl
dnl @category Misc
dnl @author Guido Draheim <guidod@gmx.de>
dnl @version 2005-12-18
dnl @license GPLWithACException

dnl AC_CHECK_FUNC_IN(HEADER, FUNCTION, [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
AC_DEFUN([AC_CHECK_FUNC_IN],
[AC_MSG_CHECKING([for $2 in $1])
AC_CACHE_VAL(ac_cv_func_$2,
[AC_TRY_LINK(
dnl Don't include <ctype.h> because on OSF/1 3.0 it includes <sys/types.h>
dnl which includes <sys/select.h> which contains a prototype for
dnl select.  Similarly for bzero.
[/* System header to define __stub macros and hopefully few prototypes,
    which can conflict with char $2(); below.  */
#include <assert.h>
#include <$1>
/* Override any gcc2 internal prototype to avoid an error.  */
]ifelse(AC_LANG, CPLUSPLUS, [#ifdef __cplusplus
extern "C"
#endif
])dnl
[/* We use char because int might match the return type of a gcc2
    builtin and then its argument prototype would still apply.  */
char $2();
], [
/* The GNU C library defines this for functions which it implements
    to always fail with ENOSYS.  Some functions are actually named
    something starting with __ and the normal name is an alias.  */
#if defined (__stub_$2) || defined (__stub___$2)
choke me
#else
$2();
#endif
], eval "ac_cv_func_$2=yes", eval "ac_cv_func_$2=no")])
if eval "test \"`echo '$ac_cv_func_'$2`\" = yes"; then
  AC_MSG_RESULT(yes)
  ifelse([$3], , :, [$3])
else
  AC_MSG_RESULT(no)
ifelse([$4], , , [$4
])dnl
fi
])

dnl AC_CHECK_FUNCS_IN(HEADER, FUNCTION... [, ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
AC_DEFUN([AC_CHECK_FUNCS_IN],
[for ac_func in $2
do
AC_CHECK_FUNC_IN($1, $ac_func,
  ac_tr_func=HAVE_`echo $ac_func | sed -e 'y:abcdefghijklmnopqrstuvwxyz:ABCDEFGHIJKLMNOPQRSTUVWXYZ:' -e 's:[[^A-Z0-9]]:_:g'`
  AC_DEFINE_UNQUOTED($ac_tr_func) $3], $4)dnl
done
])
