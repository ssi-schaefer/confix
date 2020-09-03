dnl @synopsis ACLTX_PROG_PNMTOPS([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a pnmtops application and set the variable pnmtops
dnl to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_PNMTOPS],[
AC_CHECK_PROGS(pnmtops,[pnmtops],no)
if test $pnmtops = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the pnmtops application])],
        $1)
fi
])
