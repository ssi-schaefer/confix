dnl @synopsis RSSH_CHECK_SUNPRO_C([ACTION-IF-YES],[ACTION-IF-NOT])
dnl
dnl Check whether we are using SUN workshop C compiler. The
dnl corresponding cache values is rssh_cv_check_sunpro_c, which is set
dnl to "yes" or "no" respectively.
dnl
dnl @category InstalledPackages
dnl @author Ruslan Shevchenko <Ruslan@Shevchenko.Kiev.UA>
dnl @version 2000-07-19
dnl @license AllPermissive

AC_DEFUN([RSSH_CHECK_SUNPRO_C],
[AC_CACHE_CHECK([whether using Sun Worckshop C compiler],
                [rssh_cv_check_sunpro_c],

[AC_LANG_SAVE
 AC_LANG_C
 AC_TRY_COMPILE([],
[#ifndef __SUNPRO_C
# include "error: this is not Sun Workshop."
#endif
],
               rssh_cv_check_sunpro_c=yes,
                rssh_cv_check_sunpro_c=no)
AC_LANG_RESTORE])
if test ${rssh_cv_check_sunpro_c} = yes
then
  $2
else
  $3
fi
])dnl
