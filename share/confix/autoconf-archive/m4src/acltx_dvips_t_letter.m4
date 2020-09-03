dnl @synopsis ACLTX_DVIPS_T_LETTER
dnl
dnl check if dvips accept -t letter
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([AC_LATEX_DVIPS_T_LETTER],[
ACLTX_DVIPS_T(letter,dvips_t_letter)
if test $dvips_t_letter = "no";
then
    AC_MSG_ERROR([Unable to find the -t letter option in dvips])
fi
])
