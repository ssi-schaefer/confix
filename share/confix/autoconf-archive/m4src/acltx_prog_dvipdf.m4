dnl @synopsis ACLTX_PROG_DVIPDF([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a dvipdf application and set the variable dvipdf to
dnl the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl It is possible to set manually the program to use using dvipdf=...
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_DVIPDF],[
AC_ARG_VAR(dvipdf,[specify default dvipdf application])
if test "$ac_cv_env_dvipdf_set" = "set" ; then
    AC_MSG_CHECKING([Checking for dvipdf])
    dvipdf="$ac_cv_env_dvipdf_value";
    AC_MSG_RESULT([$dvipdf (from parameter)])
else

AC_CHECK_PROGS(dvipdf,[dvipdf dvipdfm dvipdft],no)
if test $dvipdf = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the dvipdf application])],
        $1)
fi
])
