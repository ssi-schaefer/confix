dnl @synopsis ACLTX_PROG_JPEG2PS([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a jpeg2ps application and set the variable jpeg2ps
dnl to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_JPEG2PS],[
AC_CHECK_PROGS(jpeg2ps,[jpeg2ps],no)
if test $jpeg2ps = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the jpeg2ps application])],
        $1)
fi
])
