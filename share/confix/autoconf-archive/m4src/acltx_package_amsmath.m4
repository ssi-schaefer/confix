dnl @synopsis ACLTX_PACKAGE_AMSMATH
dnl
dnl This macro check for a way to include amsmath and set amsmath to
dnl this way
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PACKAGE_AMSMATH],[
AC_REQUIRE([ACLTX_DEFAULT_CLASS])
AC_CACHE_CHECK([for amsmath],[ac_cv_latex_package_f_amsmath],[
_ACLTX_TEST([\documentclass{$defaultclass}
\usepackage{amsmath,amsfonts}
\begin{document}
\end{document}],[ac_cv_latex_package_f_amsmath])
if test $ac_cv_latex_package_f_amsmath = "yes" ;
then
    [ac_cv_latex_package_f_amsmath]="\\usepackage{amsmath,amsfonts}" ; export [ac_cv_latex_package_f_amsmath] ;
else
    _ACLTX_TEST([
    \documentclass{$defaultclass}
    \usepackage{amstex}
    \begin{document}
    \end{document}
    ],[ac_cv_latex_package_f_amsmath])
    if test $ac_cv_latex_package_f_amsmath = "yes" ;
    then
        [ac_cv_latex_package_f_amsmath]="\\usepackage{amstex}" ; export [ac_cv_latex_package_f_amsmath] ;
    else
        AC_MSG_ERROR([Unable to find amsmath])
    fi
fi
])
amsmath=$[ac_cv_latex_package_f_amsmath]; export amsmath;
AC_SUBST(amsmath)
])
