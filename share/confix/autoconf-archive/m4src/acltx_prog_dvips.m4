dnl @synopsis ACLTX_PROG_DVIPS([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a dvips application and set the variable dvips to
dnl the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl It is possible to set manually the program to use using dvips=...
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_DVIPS],[
AC_ARG_VAR(dvips,[specify default dvips application])
if test "$ac_cv_env_dvips_set" = "set" ; then
    AC_MSG_CHECKING([Checking for dvips])
    dvips="$ac_cv_env_dvips_value";
    AC_MSG_RESULT([$dvips (from parameter)])
else
    AC_CHECK_PROGS(dvips,dvips,no)
fi
if test $dvips = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the dvips application])],
        $1)
fi
])
