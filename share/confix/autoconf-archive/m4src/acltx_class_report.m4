dnl @synopsis ACLTX_CLASS_REPORT([ACTION-IF-NOT-FOUND])
dnl
dnl This macro test if class report is installed and fail (default)
dnl with a error message if not
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_CLASS_REPORT],[
ACLTX_CLASS(report,report,[],[m4_ifval([$1],[$1],AC_MSG_ERROR([Unable to find the report class]))])
])
