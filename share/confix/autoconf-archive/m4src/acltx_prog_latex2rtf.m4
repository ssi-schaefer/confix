dnl @synopsis ACLTX_PROG_LATEX2RTF([ACTION-IF-NOT-FOUND])
dnl
dnl This macro find a latex2rtf application and set the variable
dnl latex2rtf to the name of the application or to no if not found if
dnl ACTION-IF-NOT-FOUND is not specified, configure fail when then
dnl application is not found.
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PROG_LATEX2RTF],[
AC_CHECK_PROGS(latex2rtf,[latex2rtf],no)
if test $latex2rtf = "no" ;
then
	ifelse($#,0,[AC_MSG_ERROR([Unable to find the latex2rtf application])],
        $1)
fi
])
