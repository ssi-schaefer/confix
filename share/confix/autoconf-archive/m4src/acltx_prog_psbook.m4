dnl @synopsis ACLTX_PROG_PSBOOK([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a psbook application and set the variable psbook to
dnl the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_PSBOOK],[
AC_CHECK_PROGS(psbook,[psbook],no)
if test $psbook = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the psbook application])],
        $1)
fi
])
