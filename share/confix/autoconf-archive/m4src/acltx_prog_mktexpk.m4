dnl @synopsis ACLTX_PROG_MKTEXPK
dnl
dnl This macro find a mktexpk application and set the variable mktexpk
dnl to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_MKTEXPK],[
AC_CHECK_PROGS(mktexpk,mktexpk,no)
if test $mktexpk = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the mktexpk application])],
        $1)
fi
])
