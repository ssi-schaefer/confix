dnl @synopsis ACLTX_PROG_GZIP([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a gzip application and set the variable gzip to the
dnl name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_GZIP],[
AC_CHECK_PROGS(gzip,[gzip],no)
if test $gzip = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the gzip application])],
        $1)
fi
])
