dnl @synopsis ACLTX_PROG_PSTOPS([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a pstops application and set the variable pstops to
dnl the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl It is possible to set manually the program to use using pstops=...
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_PSTOPS],[
AC_ARG_VAR(pstops,[specify default pstops application])
if test "$ac_cv_env_pstops_set" = "set" ; then
    AC_MSG_CHECKING([Checking for pstops])
    pstops="$ac_cv_env_pstops_value";
    AC_MSG_RESULT([$pstops (from parameter)])
else
    AC_CHECK_PROGS(pstops,[pstops],no)
fi
if test $pstops = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the pstops application])],
        $1)
fi
])
