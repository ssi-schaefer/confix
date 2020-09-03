dnl @synopsis ACLTX_PROG_PSRESIZE([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a psresize application and set the variable
dnl psresize to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_PSRESIZE],[
AC_CHECK_PROGS(psresize,[psresize],no)
if test $psresize = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the psresize application])],
        $1)
fi])
