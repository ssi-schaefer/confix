dnl @synopsis ACLTX_CLASS_BOOK([ACTION-IF-NOT-FOUND])
dnl
dnl This macro test if class book is installed and fail (default) with
dnl a error message if not
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_CLASS_BOOK],[
ACLTX_CLASS(book,book,[],[m4_ifval([$1],[$1],AC_MSG_ERROR([Unable to find the book class]))])
])
