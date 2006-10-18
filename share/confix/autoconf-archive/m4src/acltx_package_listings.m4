dnl @synopsis ACLTX_PACKAGE_LISTINGS
dnl
dnl Check if the package listings exists and set listings to yes or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

AC_DEFUN([ACLTX_PACKAGE_LISTINGS],[
    AC_REQUIRE([ACLTX_DEFAULT_CLASS])
AC_CACHE_CHECK([for listings with class $defaultclass],[ac_cv_latex_package_f_listings],[
_ACLTX_TEST([changequote(*, !)dnl
\documentclass{$defaultclass}
\usepackage{listings}
\begin{document}
\end{document}dnl
changequote([, ])],[ac_cv_latex_package_f_listings])
])
listings=$[ac_cv_latex_package_f_listings]; export listings;
AC_SUBST(listings)

])
