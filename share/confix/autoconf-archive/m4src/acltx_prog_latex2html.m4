dnl @synopsis ACLTX_PROG_LATEX2HTML([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a latex2html application and set the variable
dnl latex2html to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_LATEX2HTML],[
AC_CHECK_PROGS(latex2html,[latex2html],no)
if test $latex2html = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the latex2html application])],
        $1)
fi
])
