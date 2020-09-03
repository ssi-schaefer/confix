dnl @synopsis ACLTX_PACKAGE_LISTINGS_LANGUAGE(LANGUAGE,VARIABLETOSET)
dnl
dnl Test if the package listings accept the language LANGUAGE and set
dnl VARIABLETOSET to yes or no
dnl
dnl @category LaTeX
dnl @author Boretti Mathieu <boretti@eig.unige.ch>
dnl @version 2006-07-16
dnl @license LGPL

define(_ACLTX_PACKAGE_LANGUAGE_INTERNE,[
changequote(*, !)dnl
\documentclass{$defaultclass}
\usepackage{listings}
\lstset{language={$1}}
\begin{document}
\end{document}
changequote([, ])dnl
])

AC_DEFUN([ACLTX_PACKAGE_LISTINGS_LANGUAGE],[
AC_REQUIRE([ACLTX_PACKAGE_LISTINGS])
AC_CACHE_CHECK([for $1 language in package listings with class book],[ac_cv_latex_listings_langugae_]translit($1,[-],[_]),[
_ACLTX_TEST([
_ACLTX_PACKAGE_LANGUAGE_INTERNE($1)
],[ac_cv_latex_listings_langugae_]translit($1,[-],[_]))
])
$2=$[ac_cv_latex_listings_langugae_]translit($1,[-],[_]); export $2;
AC_SUBST($2)
])
