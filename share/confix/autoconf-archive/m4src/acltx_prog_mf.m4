dnl @synopsis ACLTX_PROG_MF([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a mf application and set the variable mf to the
dnl name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl It is possible to set manually the program to use using mf=...
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_MF],[
AC_ARG_VAR(mf,[specify default mf application])
if test "$ac_cv_env_mf_set" = "set" ; then
    AC_MSG_CHECKING([Checking for mf])
    mf="$ac_cv_env_mf_value";
    AC_MSG_RESULT([$mf (from parameter)])
else
    AC_CHECK_PROGS(mf,[mf mfw mf-nowin],no)
fi
if test $mf = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the mf application])],
        $1)
fi
])
